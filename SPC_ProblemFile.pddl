(define (problem SPCProblem) (:domain SPCDomain)

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
	(FanOn Fan)

	(IRHigh IRSensor)
	(DoorOpen Door)
	(UltrasonicHigh UltrasonicSensor)
)

(:goal  (and (TempSuitable TempSensor) (LuminositySuitable LightSensor) (DoorSuitable Door) (suitable UltrasonicSensor));Turn on LED to indicate free spot
)
)