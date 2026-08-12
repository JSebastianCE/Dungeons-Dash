using UnrealBuildTool;
using System.Collections.Generic;

public class DungeonsAndDashTarget : TargetRules
{
    public DungeonsAndDashTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        ExtraModuleNames.Add("DungeonsAndDash");
    }
}
