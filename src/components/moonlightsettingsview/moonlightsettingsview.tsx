import { DialogBody, DialogControlsSection, DialogControlsSectionHeader, Field, Focusable } from "@decky/ui";
import { LabelWithIcon, NumericTextInput, ResolutionSelectionDropdown, ToggleField } from "../shared";
import { ModifyListButton, RemoveListEntryButton } from "../shared/indexedlist";
import { SettingsManager, minBitrate, minFps } from "../../lib";
import { AppResolutionOverrideDropdown } from "./appresolutionoverridedropdown";
import { FC } from "react";
import { HostOff } from "../icons";
import { LinkedDisplayList } from "./linkeddisplaylist";
import { ModifyResolutionModal } from "./modifyresolutionmodal";
import { MoonlightExecutableSelection } from "./moonlightexecutableselection";
import { useCurrentHostSettings } from "../../hooks";

interface Props {
  settingsManager: SettingsManager;
}

export const MoonlightSettingsView: FC<Props> = ({ settingsManager }) => {
  const hostSettings = useCurrentHostSettings(settingsManager);
  if (hostSettings === null) {
    return (
      <DialogBody>
        <DialogControlsSection>
          <Field
            label={<LabelWithIcon icon={HostOff} label="HOST IS NOT SELECTED" />}
            description="Go to host selection page to select host"
            bottomSeparator="none" />
        </DialogControlsSection>
      </DialogBody>
    );
  }

  return (
    <DialogBody>
      <DialogControlsSection>
        <DialogControlsSectionHeader>General</DialogControlsSectionHeader>
        <MoonlightExecutableSelection settingsManager={settingsManager} />
        <Field
          label="Default bitrate in kbps (optional)"
          description="Bitrate to be applied when starting stream. Will be overridden by the one from custom resolution if provided."
          childrenContainerWidth="fixed"
        >
          <NumericTextInput
            min={minBitrate}
            optional={true}
            value={hostSettings.resolution.defaultBitrate}
            setValue={(value) => settingsManager.updateHost((hostSettings) => { hostSettings.resolution.defaultBitrate = value; })}
          />
        </Field>
        <Field
          label="Default FPS (optional)"
          description="FPS to be applied when starting stream. Will be overridden by the one from custom resolution if provided. Providing FPS without bitrate will trigger Moonlight to automatically calculate the bitrate!"
          childrenContainerWidth="fixed"
        >
          <NumericTextInput
            min={minFps}
            optional={true}
            value={hostSettings.resolution.defaultFps}
            setValue={(value) => settingsManager.updateHost((hostSettings) => { hostSettings.resolution.defaultFps = value; })}
          />
        </Field>
        <ToggleField
          label="Pass the resolution, bitrate and FPS options to Moonlight to use instead of Moonlight's default ones"
          description="Disable this if you want to use the settings from the Moonlight app itself"
          value={hostSettings.resolution.passToMoonlight}
          setValue={(value) => settingsManager.updateHost((hostSettings) => { hostSettings.resolution.passToMoonlight = value; })}
        />
      </DialogControlsSection>
      <DialogControlsSection>
        <DialogControlsSectionHeader>Custom Resolution</DialogControlsSectionHeader>
        <Field
          description={
            <>
              <div>Here you can define custom resolution which is used by MoonDeck to enhance gaming experience.</div>
              <br />
              <div>See the sections below this one for more information for where it can be used.</div>
            </>
          }
          focusable={true}
        />
        <ToggleField
          label="Use SteamDeck's primary resolution as fallback"
          description="If custom resolution is disabled, SteamDeck's primary resolution will be used - that of internal or external display."
          value={hostSettings.resolution.automatic}
          setValue={(value) => settingsManager.updateHost((hostSettings) => { hostSettings.resolution.automatic = value; })}
        />
        <ToggleField
          label="Use custom resolution from the list"
          description="This setting has no effect if the custom resolution list is empty."
          value={hostSettings.resolution.useCustomDimensions}
          setValue={(value) => settingsManager.updateHost((hostSettings) => { hostSettings.resolution.useCustomDimensions = value; })}
        />
        <Field
          label="Selected custom resolution"
          childrenContainerWidth="fixed"
          bottomSeparator="none"
        >
          <ResolutionSelectionDropdown
            currentIndex={hostSettings.resolution.selectedDimensionIndex}
            currentList={hostSettings.resolution.dimensions}
            setIndex={(value) => { settingsManager.updateHost((hostSettings) => { hostSettings.resolution.selectedDimensionIndex = value; }); }}
          />
        </Field>
        <Field
          childrenContainerWidth="fixed"
          childrenLayout="below"
        >
          <Focusable style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
            <ModifyListButton
              modal={ModifyResolutionModal}
              currentList={hostSettings.resolution.dimensions}
              currentIndex={null}
              updateList={(list, index) => {
                settingsManager.updateHost((hostSettings) => {
                  hostSettings.resolution.dimensions = list;
                  hostSettings.resolution.selectedDimensionIndex = index;
                });
              }}
            />
            <ModifyListButton
              modal={ModifyResolutionModal}
              currentList={hostSettings.resolution.dimensions}
              currentIndex={hostSettings.resolution.selectedDimensionIndex}
              updateList={(list, index) => {
                settingsManager.updateHost((hostSettings) => {
                  hostSettings.resolution.dimensions = list;
                  hostSettings.resolution.selectedDimensionIndex = index;
                });
              }}
            />
            <RemoveListEntryButton
              currentList={hostSettings.resolution.dimensions}
              currentIndex={hostSettings.resolution.selectedDimensionIndex}
              updateList={(list, index) => {
                settingsManager.updateHost((hostSettings) => {
                  hostSettings.resolution.dimensions = list;
                  hostSettings.resolution.selectedDimensionIndex = index;
                });
              }}
            />
          </Focusable>
        </Field>
        <LinkedDisplayList hostSettings={hostSettings} settingsManager={settingsManager} />
      </DialogControlsSection>
      <DialogControlsSection>
        <DialogControlsSectionHeader>App Resolution Override</DialogControlsSectionHeader>
        <Field
          description={
            <>
              <div>Sets the app shortcut resolution property which informs the Gamescope on how to perform scaling.</div>
              <br />
              <div>Note: this applies ONLY for the external displays (technically you can enable it for internal display too, but we don't do it).</div>
            </>
          }
          bottomSeparator="none"
          focusable={true}
        />
        <Field
          description={
            <>
              <div>The following options are available:</div>
              <div>&bull; "Custom Resolution" (MoonDeck's default) - if custom resolution is enabled and selected, it will be used for scaling.</div>
              <div>&bull; "Display Resolution" - will use the resolution of the primary display for scaling.</div>
              <div>&bull; "Native" - technically should be the same as "Display Resolution", however one user reported that it still performs some unnecessary scaling once the stream starts.</div>
              <div>&bull; "Default" - this is the Valve's default scaling option. It is just bad...</div>
              <br />
              <div>If for whatever reason MoonDeck fails to retrieve either a custom resolution (because it's disabled) or the display resolution, the following fallback chain will ensure that at least something is set:</div>
              <div>"Custom Resolution" -&gt; "Display Resolution" -&gt; "Native"</div>
            </>
          }
          focusable={true}
        />
        <Field
          label="Selected override"
          childrenContainerWidth="fixed"
        >
          <AppResolutionOverrideDropdown
            currentOverride={hostSettings.resolution.appResolutionOverride}
            setOverride={(value) => { settingsManager.updateHost((hostSettings) => { hostSettings.resolution.appResolutionOverride = value; }); }}
          />
        </Field>
      </DialogControlsSection>
    </DialogBody>
  );
};
