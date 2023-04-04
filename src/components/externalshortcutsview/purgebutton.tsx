import { AppDetails, ConfirmModal, DialogButton, showModal } from "decky-frontend-lib";
import { logger, removeShortcut, restartSteamClient } from "../../lib";
import { VFC } from "react";

interface Props {
  shortcuts: AppDetails[];
}

async function purgeShortcuts(shortcuts: AppDetails[]): Promise<void> {
  for (const detail of shortcuts) {
    await removeShortcut(detail.unAppID);
  }

  if (shortcuts.length > 0) {
    restartSteamClient();
  }
}

export const PurgeButton: VFC<Props> = ({ shortcuts }) => {
  const handleClick = (): void => {
    showModal(
      <ConfirmModal
        strTitle="Are you sure you want to purge?"
        strDescription="This action cannot be undone."
        onOK={() => { purgeShortcuts(shortcuts).catch((e) => logger.critical(e)); }}
      />
    );
  };

  return (
    <DialogButton disabled={shortcuts.length === 0} onClick={() => handleClick()}>
      Purge
    </DialogButton>
  );
};
