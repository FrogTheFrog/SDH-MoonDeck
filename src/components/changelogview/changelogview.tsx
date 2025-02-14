import { DialogBody, DialogControlsSection, Field } from "@decky/ui";
import { FC } from "react";

export const ChangelogView: FC<unknown> = () => {
  return (
    <DialogBody>
      <DialogControlsSection>
        <Field
          label="1.9.0"
          description={
            <>
              <div>&bull; TODO Removed the resolution change option completely.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.8.5"
          description="Added MoonDeck button for betas."
          focusable={true}
        />
        <Field
          label="1.8.4"
          description={
            <>
              <div>&bull; Deprecated the resolution change for linux and removed it for Windows.</div>
              <div>&bull; Added MoonDeck button for demos.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.8.3"
          description="Added python executable override to be used for a runner script (for immutable distros without required system packages)."
          focusable={true}
        />
        <Field
          label="1.8.2"
          description="Fixed exception (introduced with 1.8.1) when a fresh settings file is being created."
          focusable={true}
        />
        <Field
          label="1.8.1"
          description={
            <>
              <div>&bull; Added an optional prompt to confirm whether you really want to start the stream or not.</div>
              <div>&bull; Removed the WOL broadcast for IPv6.</div>
              <div>&bull; Added an option to configure Steam Input state for external controllers.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.8.0"
          description={
            <>
              <div>&bull; Migrate plugin to use new Decky API.</div>
              <div>&bull; Sunshine app sync button can now be added to the Quick Access Menu.</div>
              <div>&bull; Last used app resolution override will be used when adding new Sunshine apps.</div>
              <div>&bull; MoonDeck shortcuts can now be disabled if only Sunshine apps are needed.</div>
              <div>&bull; Removed fps and bitrate limits.</div>
              <div>&bull; Fix IPv6 handling for WOL.</div>
              <div>&bull; Expose more runner timeout settings.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.7.1"
          description={
            <>
              <div>&bull; Sunshine app generator will now use custom Moonlight executable if selected.</div>
              <div>&bull; Sunshine app generator now properly escapes hostname and app name.</div>
              <div>&bull; Exotic hostnames with HTML characters are now properly parsed.</div>
              <div>&bull; Added an option to set z-index to the button.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.7.0"
          description="Fixed incoming breaking change from Sunshine (mac address no longer being exposed via HTTP port). Requires new Buddy 1.6.0 version!"
          focusable={true}
        />
        <Field
          label="1.6.17"
          description={
            <>
              <div>&bull; Migrated plugin to use global DFL version.</div>
              <div>&bull; Fixed issue where MoonDeckStream would close on host when stream is terminated (in some cases).</div>
              <div>&bull; Moonlight log is now properly written to (tnx python for this stupid non-sense).</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.16"
          description={
            <>
              <div>&bull; Updated MobX patching strategy. Nothing observable, just some errors are gone...</div>
              <div>&bull; Bumped DFL version.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.15"
          description={
            <>
              <div>&bull; Activated host selection dropdown even when there is only 1 host in QAM, so that the navigation is less broken.</div>
              <div>&bull; Added a setting for a custom Moonlight executable (AppImage or whatever).</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.14"
          description={
            <>
              <div>&bull; Fix issues with MobX@6 on beta.</div>
              <div>&bull; Moved settings button to be inline with the title.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.13"
          description={
            <>
              <div>&bull; Fixed round CSS style not applying to the MoonDeck button.</div>
              <div>&bull; Added auto-WOL functionality. Can be disabled in the runner settings.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.12"
          description="Added a feature to link display to custom resolution. The resolution is then automatically selected before starting stream."
          focusable={true}
        />
        <Field
          label="1.6.11"
          description={
            <>
              <div>&bull; Added a wait with timeout for stream to end after a successful session so that Sunshine can cleanup properly.</div>
              <div>&bull; Removed the IP restriction for static address - you can now use domain names.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.10"
          description={
            <>
              <div>&bull; Added a dropdown for selecting hosts in quick access menu.</div>
              <div>&bull; Fixed a bug where a host might be added automatically as a new host entry if the server's id changes.</div>
              <div>&bull; Fixed some minor UI bugs.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.9"
          description={
            <>
              <div>&bull; Added options to override various timeouts in runner script and also to enable debug logs.</div>
              <div>&bull; Added option to override FPS in Moonlight.</div>
              <div>&bull; Grouped, split and renamed various MoonDeck configuration pages.</div>
              <div>&bull; Bitrate (and FPS) can now be overridden without specifying custom resolution.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.8"
          description="Adding missing dependencies/handling some edge cases to make plugin more compatible with other linux distros."
          focusable={true}
        />
        <Field
          label="1.6.7"
          description="Remove the leftover error from 1.6.6 release."
          focusable={true}
        />
        <Field
          label="1.6.6"
          description="Fixed the breaking changes on stable (could not add new shortcuts once again)."
          focusable={true}
        />
        <Field
          label="1.6.5"
          description="Fixed the breaking changes on beta (could not add new shortcuts)."
          focusable={true}
        />
        <Field
          label="1.6.4"
          description="Fixed a bug where you could not select custom resolution in Sunshine Apps page if there was only 1 resolution entry in the list."
          focusable={true}
        />
        <Field
          label="1.6.3"
          description="Increase compatibility with other plugins, like Game Theme Music."
          focusable={true}
        />
        <Field
          label="1.6.2"
          description={
            <>
              <div>&bull; Gamestream server port is no longer hard-coded and will now be properly detected or can be entered when adding host manually.</div>
              <div>&bull; Bumped DFL version.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.1"
          description={
            <>
              <div>&bull; Make the plugin more compatible with other plugins that inject into app page (no more 'null' error pages).</div>
              <div>&bull; Make MoonDeck more game-launcher friendly (like EALink).</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.6.0"
          description={
            <>
              <div>&bull; Added a new feature to sync Sunshine apps with MoonDeck (breaking change).</div>
              <div>&bull; Updated decky's frontend lib version.</div>
              <div>&bull; Fixed some typos and descriptions.</div>
              <div>&bull; Added better logging on python backend.</div>
              <div>&bull; Added "pass to Moonlight" option in in QAM.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.5.9"
          description={
            <>
              <div>&bull; Separated resolution options into separate sections.</div>
              <div>&bull; Added an option not to pass the resolution to Buddy in case you want to use do/undo in Sunshine for changing resolution.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.5.8"
          description="Added app resolution override handling feature. Options can be found in host settings."
          focusable={true}
        />
        <Field
          label="1.5.7"
          description={
            <>
              <div>&bull; Fixed some UI bugs when modifying host settings.</div>
              <div>&bull; Added an option in the host settings to use custom app name for gamestream.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.5.6"
          description="Updated dependency to Decky's Frontend Library."
          focusable={true}
        />
        <Field
          label="1.5.5"
          description="Fixed breaking changes from Valve."
          focusable={true}
        />
        <Field
          label="1.5.4"
          description={
            <>
              <div>&bull; Enabled saving of Moonlight output for easier debugging.</div>
              <div>&bull; Branch will no longer be specified for Moonlight. The default one (stable or beta) will be selected by flatpak.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.5.3"
          description={
            <>
              <div>&bull; Added an option to override default bitrate.</div>
              <div>&bull; Added links to MoonDeck's wiki page.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.5.2"
          description="Resolution change (if any) is now done before the gamestream is started for more stability."
          focusable={true}
        />
        <Field
          label="1.5.1"
          description="Bumped DFL version to fix incoming breaking changes from Valve."
          focusable={true}
        />
        <Field
          label="1.5.0"
          description={
            <>
              <div>&bull; MoonDeck app can now run alongside other apps. Might be useful with the new multitasking support/bugfix on Steam.</div>
              <div>&bull; Added an option (enabled by default) not to close the Steam once the gaming session ends successfully.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.4.1"
          description="Fixed an issue where valid expections are treated as invalid. As a result the log file would grow big."
          focusable={true}
        />
        <Field
          label="1.4.0"
          description={
            <>
              <div>&bull; Changed the underlying communication protocol with Buddy to HTTPS (should have no user impact).</div>
              <div>&bull; Invalidated SSL keys to force update to the new Buddy version, since the legacy version check will not work.</div>
              <div>&bull; Added an option to suspend (put to sleep) host PC.</div>
              <div>&bull; Custom resolution now takes priority over automatic one since it mostly detects native resolution even with external display.</div>
              <div>&bull; Multiple custom resolutions can be saved now per host.</div>
              <div>&bull; Custom resolution can now be toggled and selected in quick access menu (if there is at least 1 list entry).</div>
              <div>&bull; Removed early resolution change option as it is a leftover from NVidia times.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.3.0"
          description={
            <>
              <div>&bull; Added this changelog page.</div>
              <div>&bull; Discontinued support for NVidia's Gamestream service.</div>
              <div>&bull; Added support for Sunshine's Gamestream service. New instructions need to be followed to setup Buddy again!</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.2.0"
          description={
            <>
              <div>&bull; Added option to manually enter host IP address.</div>
              <div>&bull; Fixed broken modals by updating DFL.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.1.0"
          description={
            <>
              <div>&bull; Added resolution options per host.</div>
              <div>&bull; Fixed issues with with plugin not initalizing in beta.</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="1.0.0"
          description="Initial release."
          focusable={true}
        />
      </DialogControlsSection>
    </DialogBody>
  );
};
