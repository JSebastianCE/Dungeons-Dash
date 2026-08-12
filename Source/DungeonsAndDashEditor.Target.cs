using UnrealBuildTool;
using System.Collections.Generic;

public class DungeonsAndDashEditorTarget : TargetRules
{
    public DungeonsAndDashEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        ExtraModuleNames.Add("DungeonsAndDash");
    }
}
