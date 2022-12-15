import { HostSettings, SettingsManager } from "./settingsmanager";
import { BehaviorSubject } from "rxjs";
import { BuddyProxy } from "./buddyproxy";
import { Mutex } from "async-mutex";
import { ReadonlySubject } from "./readonlysubject";
import { ServerAPI } from "decky-frontend-lib";
import { logger } from "./logger";

export interface GameStreamHost {
  address: string;
  hostName: string;
  mac: string;
  uniqueId: string;
}

export type ServerStatus = "Offline" | "Online";
export type PairingStartStatus = "AlreadyPaired" | "VersionMismatch" | "NoClientId" | "Pairing" | "Offline" | "Failed" | "PairingStarted";

async function scanForHosts(serverAPI: ServerAPI, timeout: number): Promise<GameStreamHost[]> {
  try {
    const resp = await serverAPI.callPluginMethod<{ timeout: number }, GameStreamHost[]>("scan_for_hosts", { timeout });
    if (resp.success) {
      return resp.result;
    } else {
      logger.error("Error while scanning for hosts: " + resp.result);
    }
  } catch (message) {
    logger.critical(message);
  }
  return [];
}

async function findHost(serverAPI: ServerAPI, hostId: string, timeout: number): Promise<GameStreamHost | null> {
  try {
    const resp = await serverAPI.callPluginMethod<{ host_id: string; timeout: number }, GameStreamHost | null>("find_host", { host_id: hostId, timeout });
    if (resp.success) {
      return resp.result;
    } else {
      logger.error("Error while finding host: " + resp.result);
    }
  } catch (message) {
    logger.critical(message);
  }
  return null;
}

async function getServerInfo(serverAPI: ServerAPI, address: string, timeout: number): Promise<GameStreamHost | null> {
  try {
    const resp = await serverAPI.callPluginMethod<{ address: string; timeout: number }, GameStreamHost | null>("get_server_info", { address, timeout });
    if (resp.success) {
      return resp.result;
    } else {
      logger.error("Error while getting server info: " + resp.result);
    }
  } catch (message) {
    logger.critical(message);
  }
  return null;
}

async function startPairing(serverAPI: ServerAPI, address: string, buddyPort: number, clientId: string, pin: number, timeout: number): Promise<PairingStartStatus> {
  try {
    const resp = await serverAPI.callPluginMethod<{ address: string; buddy_port: number; client_id: string; pin: number; timeout: number }, PairingStartStatus>("start_pairing", { address, buddy_port: buddyPort, client_id: clientId, pin, timeout });
    if (resp.success) {
      return resp.result;
    } else {
      logger.error("Error while pairing with buddy: " + resp.result);
    }
  } catch (message) {
    logger.critical(message);
  }
  return "Offline";
}

async function abortPairing(serverAPI: ServerAPI, address: string, buddyPort: number, clientId: string, timeout: number): Promise<void> {
  try {
    const resp = await serverAPI.callPluginMethod<{ address: string; buddy_port: number; client_id: string; timeout: number }, null>("abort_pairing", { address, buddy_port: buddyPort, client_id: clientId, timeout });
    if (!resp.success) {
      logger.error("Error while aborting pairing: " + resp.result);
    }
  } catch (message) {
    logger.critical(message);
  }
}

export class ServerProxy {
  private readonly serverAPI: ServerAPI;
  private readonly settingsManager: SettingsManager;
  private readonly buddyProxy: BuddyProxy;

  private readonly mutex = new Mutex();
  private readonly statusSubject = new BehaviorSubject<ServerStatus>("Offline");
  private readonly refreshingSubject = new BehaviorSubject<boolean>(false);

  readonly status = new ReadonlySubject(this.statusSubject);
  readonly refreshing = new ReadonlySubject(this.refreshingSubject);

  private updateHostSettingsUnlocked(host: GameStreamHost, selectHost: boolean, staticAddress: boolean | null): void {
    this.settingsManager.update((settings) => {
      const currentSettings = settings.hostSettings[host.uniqueId] ?? null;
      const hostSettings: HostSettings = {
        buddyPort: currentSettings?.buddyPort ?? 59999,
        address: host.address,
        staticAddress: staticAddress ?? (currentSettings?.staticAddress ?? false),
        hostName: host.hostName,
        mac: host.mac,
        resolution: {
          automatic: currentSettings?.resolution.automatic ?? true,
          earlyChangeEnabled: currentSettings?.resolution.earlyChangeEnabled ?? true,
          passToMoonlight: currentSettings?.resolution.passToMoonlight ?? true,
          useCustomDimensions: currentSettings?.resolution.useCustomDimensions ?? false,
          customWidth: currentSettings?.resolution.customWidth ?? 1280,
          customHeight: currentSettings?.resolution.customHeight ?? 800
        }
      };

      settings.currentHostId = selectHost ? host.uniqueId : settings.currentHostId;
      settings.hostSettings[host.uniqueId] = hostSettings;
    });
  }

  private updateStatus(newStatus: ServerStatus): void {
    if (this.statusSubject.value !== newStatus) {
      this.statusSubject.next(newStatus);
    }
  }

  constructor(serverAPI: ServerAPI, settingsManager: SettingsManager, buddyProxy: BuddyProxy) {
    this.serverAPI = serverAPI;
    this.settingsManager = settingsManager;
    this.buddyProxy = buddyProxy;
  }

  async refreshStatus(): Promise<void> {
    if (this.mutex.isLocked()) {
      await this.mutex.waitForUnlock();
      return;
    }

    const release = await this.mutex.acquire();
    try {
      this.refreshingSubject.next(true);

      const hostId = this.settingsManager.settings.value?.currentHostId ?? null;
      if (hostId === null) {
        this.updateStatus("Offline");
        return;
      }

      let result: GameStreamHost | null = null;
      const hostSettings = this.settingsManager.hostSettings;
      if (hostSettings) {
        result = hostSettings.staticAddress ? await getServerInfo(this.serverAPI, hostSettings.address, 1) : await findHost(this.serverAPI, hostId, 1);
      } else {
        result = await findHost(this.serverAPI, hostId, 1);
      }

      if (this.settingsManager.settings.value?.currentHostId === hostId) {
        const newStatus = result === null ? "Offline" : "Online";
        this.updateStatus(newStatus);
      }

      if (result !== null) {
        this.updateHostSettingsUnlocked(result, false, null);
      }
    } finally {
      this.refreshingSubject.next(false);
      release();
    }
  }

  async getServerInfo(address: string): Promise<GameStreamHost | null> {
    return await getServerInfo(this.serverAPI, address, 2);
  }

  async scanForHosts(): Promise<GameStreamHost[]> {
    return await scanForHosts(this.serverAPI, 5);
  }

  async startPairing(pin: number): Promise<PairingStartStatus> {
    const hostSettings = this.settingsManager.hostSettings;

    const address = hostSettings?.address ?? null;
    const buddyPort = hostSettings?.buddyPort ?? null;
    const clientId = this.settingsManager.settings.value?.clientId ?? null;

    if (address === null || buddyPort === null || clientId === null) {
      return "Offline";
    }

    const result = await startPairing(this.serverAPI, address, buddyPort, clientId, pin, 5);
    await this.buddyProxy.refreshStatus();
    return result;
  }

  async abortPairing(): Promise<void> {
    const hostSettings = this.settingsManager.hostSettings;

    const address = hostSettings?.address ?? null;
    const buddyPort = hostSettings?.buddyPort ?? null;
    const clientId = this.settingsManager.settings.value?.clientId ?? null;

    if (address === null || buddyPort === null || clientId === null) {
      return;
    }

    await abortPairing(this.serverAPI, address, buddyPort, clientId, 5);
    await this.buddyProxy.refreshStatus();
  }

  async updateHostSettings(host: GameStreamHost, selectHost: boolean, staticAddress: boolean): Promise<void> {
    const release = await this.mutex.acquire();
    try {
      this.updateHostSettingsUnlocked(host, selectHost, staticAddress);
    } finally {
      release();
    }
  }
}
