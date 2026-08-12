#include "DDOneLapFinish.h"

#include "Components/BoxComponent.h"
#include "Components/PrimitiveComponent.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PawnMovementComponent.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"
#include "Styling/CoreStyle.h"

ADDOneLapFinish::ADDOneLapFinish()
{
    PrimaryActorTick.bCanEverTick = false;
    Trigger = CreateDefaultSubobject<UBoxComponent>(TEXT("FinishTrigger"));
    SetRootComponent(Trigger);
    Trigger->SetBoxExtent(FVector(300.f, 1000.f, 500.f));
    Trigger->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
    Trigger->SetCollisionObjectType(ECC_WorldDynamic);
    Trigger->SetCollisionResponseToAllChannels(ECR_Overlap);
    Trigger->SetGenerateOverlapEvents(true);
    Trigger->SetNotifyRigidBodyCollision(true);
    Trigger->OnComponentBeginOverlap.AddDynamic(this, &ADDOneLapFinish::OnFinishOverlap);
    Trigger->OnComponentHit.AddDynamic(this, &ADDOneLapFinish::OnFinishHit);
}

void ADDOneLapFinish::OnFinishOverlap(UPrimitiveComponent*, AActor* OtherActor,
    UPrimitiveComponent*, int32, bool, const FHitResult&)
{
    FinishRace(OtherActor);
}

void ADDOneLapFinish::OnFinishHit(UPrimitiveComponent*, AActor* OtherActor,
    UPrimitiveComponent*, FVector, const FHitResult&)
{
    FinishRace(OtherActor);
}

void ADDOneLapFinish::FinishRace(AActor* VehicleActor)
{
    if (bRaceFinished || !VehicleActor) return;
    APawn* Pawn = Cast<APawn>(VehicleActor);
    if (!Pawn) Pawn = Cast<APawn>(VehicleActor->GetOwner());
    if (!Pawn) return;

    bRaceFinished = true;
    if (APlayerController* PC = Cast<APlayerController>(Pawn->GetController()))
    {
        Pawn->DisableInput(PC);
        PC->SetIgnoreMoveInput(true);
        PC->SetIgnoreLookInput(true);
    }
    if (UPawnMovementComponent* Movement = Pawn->GetMovementComponent())
    {
        Movement->StopMovementImmediately();
        Movement->Deactivate();
    }
    TArray<UPrimitiveComponent*> Primitives;
    Pawn->GetComponents(Primitives);
    for (UPrimitiveComponent* Primitive : Primitives)
    {
        if (Primitive && Primitive->IsSimulatingPhysics())
        {
            Primitive->SetPhysicsLinearVelocity(FVector::ZeroVector);
            Primitive->SetPhysicsAngularVelocityInDegrees(FVector::ZeroVector);
        }
    }

    if (GEngine && GEngine->GameViewport)
    {
        GEngine->GameViewport->AddViewportWidgetContent(
            SNew(SOverlay)
            + SOverlay::Slot().HAlign(HAlign_Fill).VAlign(VAlign_Fill)
            [SNew(SBorder).BorderBackgroundColor(FLinearColor(0.f, 0.f, 0.f, 0.72f))]
            + SOverlay::Slot().HAlign(HAlign_Center).VAlign(VAlign_Center)
            [SNew(STextBlock).Text(FText::FromString(TEXT("¡GANASTE!")))
                .Font(FCoreStyle::GetDefaultFontStyle("Bold", 96))
                .ColorAndOpacity(FLinearColor(1.f, 0.75f, 0.05f, 1.f))]
        , 1000);
    }
}
