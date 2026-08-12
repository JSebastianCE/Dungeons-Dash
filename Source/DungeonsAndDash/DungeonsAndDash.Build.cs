using UnrealBuildTool;

public class DungeonsAndDash : ModuleRules
{
    public DungeonsAndDash(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "InputCore", "Slate", "SlateCore" });
    }
}
