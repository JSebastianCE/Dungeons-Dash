#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "CodexGraphAuditLibrary.generated.h"

UCLASS()
class CODEXGRAPHAUDIT_API UCodexGraphAuditLibrary
    : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Codex")
    static FString DumpWeek7Graphs();

    UFUNCTION(BlueprintCallable, Category = "Codex")
    static FString FixWeek7HitImpulseBalance();

    UFUNCTION(BlueprintCallable, Category = "Codex")
    static FString ApplyMarioKartDriftMiniTurbo();

    UFUNCTION(BlueprintCallable, Category = "Codex")
    static FString FixMarioKartDriftRuntimeFeel();

    UFUNCTION(BlueprintCallable, Category = "Codex")
    static FString FixMarioKartPhysicsDrift();

    UFUNCTION(BlueprintCallable, Category = "Codex")
    static FString ConvertDebugHitToControlledRam();

    UFUNCTION(BlueprintCallable, Category = "Codex")
    static FString FixDriftButtonDoesNotBrake();
};
