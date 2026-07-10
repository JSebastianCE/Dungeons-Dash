using UnrealBuildTool;

public class CodexGraphAudit : ModuleRules
{
    public CodexGraphAudit(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new[]
        {
            "Core",
            "CoreUObject",
            "Engine"
        });

        PrivateDependencyModuleNames.AddRange(new[]
        {
            "UnrealEd",
            "BlueprintGraph"
        });
    }
}
