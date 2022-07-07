(define (problem ABSProblemnew) (:domain ABSSDomainnew)

(:objects 
    TempSensor - sensor
    Fan - actuator

    LightSensor - sensor
    Light - actuator

    IRSensor - sensor
    Door - actuator
    Parkingvacancy - spot
    
    UltrasonicSensor - sensor
    Led - actuator
   

)

(:init
    (TempHigh TempSensor)
    ;(FanOn Fan)
    
    ;(LuminosityHigh LightSensor)
    ;(LightOn Light)

    ;(IRHigh IRSensor)
    ;(DoorOpen Door)
    (Notmax Parkingvacancy)
    ;(UltrasonicHigh UltrasonicSensor) ;;Parking spot not occupied
    (LedOn Led)
    
)

(:goal  (and (TempSuitable TempSensor) (LuminositySuitable LightSensor) (DoorSuitable Door) (suitable UltrasonicSensor));Turn on LED to indicate free spot
)
)