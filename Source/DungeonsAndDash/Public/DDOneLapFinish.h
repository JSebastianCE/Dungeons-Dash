#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "DDOneLapFinish.generated.h"

class UBoxComponent;

UCLASS(Blueprintable)
class DUNGEONSANDDASH_API ADDOneLapFinish : public AActor
{
    GENERATED_BODY()

public:
    ADDOneLapFinish();

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Race")
    TObjectPtr<UBoxComponent> Trigger;

protected:
    UFUNCTION()
    void OnFinishOverlap(UPrimitiveComponent* Overlapped, AActor* OtherActor,
        UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep,
        const FHitResult& SweepResult);

    UFUNCTION()
    void OnFinishHit(UPrimitiveComponent* HitComponent, AActor* OtherActor,
        UPrimitiveComponent* OtherComponent, FVector NormalImpulse,
        const FHitResult& Hit);

private:
    void FinishRace(AActor* VehicleActor);
    bool bRaceFinished = false;
};
