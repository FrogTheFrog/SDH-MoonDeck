import { DialogBody, DialogControlsSection, Field } from "decky-frontend-lib";
import { VFC } from "react";

export const ChangelogView: VFC<unknown> = () => {
  return (
    <DialogBody>
      <DialogControlsSection>
        <Field
          label="1.6.0"
          description={
            <>
              <div>&bull; Added a new feature to sync Sunshine apps with MoonDeck (breaking change).</div>
              <div>&bull; Updated decky's frontend lib version.</div>
              <div>&bull; Fixed some typos and descriptions.</div>
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
