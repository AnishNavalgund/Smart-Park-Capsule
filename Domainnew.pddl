(define (domain ABSSDomainnew)

    (:requirements
        :strips
        :typing
        :negative-preconditions
        
    )

    (:types
        sensor actuator spot - object
    )

   
    (:predicates
        ;;IR sensor - to actuate the main door if there is a spot available and to increment the number of parked cars
        (IRHigh ?ih - sensor)
        ;(IRLow ?il - sensor)
        (DoorOpen ?do - actuator)
        ;(DoorClosed ?dc - actuator)
        (DoorSuitable ?md - actuator)
        (Notmax ?nm - spot)

        ;;Light Sensor to Maintain luminosity
        (LuminosityHigh ?lh - sensor) 
        ;(LuminosityLow ?ll - sensor)
        (LuminositySuitable ?ls - sensor)
        (LightOn ?lo - actuator)
        ;(LightOff ?loff - actuator)

        ;Temperature maintanance
        (TempHigh ?th - sensor)
        ;(TempLow ?tl - sensor)
        (TempSuitable ?ts - sensor)
        (FanOn ?fo - actuator)
        ;(FanOff ?o - actuator)

        (UltrasonicHigh ?uh - sensor)
        ;(UltrasonicLow ?ul - sensor)
        (Suitable ?oc - sensor)
        ;(Notsuitable ?noc - actuator)
        (LedOn ?b - actuator)
        ;(LedOff ?bo - actuator)
        ;(suitable ?su -sensor)
    )
   
    (:action Opendoor
        :parameters (?ir - sensor ?door ?Dsuit -actuator ?spot -spot)
        :precondition (and (not(IRHigh ?ir)) (not(DoorOpen ?door)) (Notmax ?spot) (not(DoorSuitable ?Dsuit)))
        :effect (and (DoorOpen ?door) (DoorSuitable ?Dsuit))
    )
    (:action Closedoor
        :parameters (?ir - sensor ?door ?Dsuit - actuator)
        :precondition (and (IRHigh ?ir) (DoorOpen ?door) (not(DoorSuitable ?Dsuit)))
        :effect (and (not(DoorOpen ?door)) (DoorSuitable ?Dsuit))
    )

    (:action SwitchOnLight
        :parameters (?lumi ?lsuit -sensor ?led -actuator)
        :precondition (and (not(LuminosityHigh ?lumi)) (not(LightOn ?led)) (not(LuminositySuitable ?lsuit)))
        :effect (and (LightOn ?led) (LuminositySuitable ?lsuit))
    )
    (:action SwitchOffLight
        :parameters (?lumi ?lsuit -sensor ?led -actuator)
        :precondition (and (LuminosityHigh ?lumi) (LightOn ?led) (not(LuminositySuitable ?lsuit)))
        :effect (and (not(LightOn ?led)) (LuminositySuitable ?lsuit))
    )

    (:action DecreaseTemperature
        :parameters (?temp ?suit -sensor ?f -actuator)
        :precondition (and (TempHigh ?temp) (not(FanOn ?f)) (not(TempSuitable ?suit)))
        :effect (and (FanOn ?f) (TempSuitable ?suit))
    )
    (:action IncreaseTemperature
        :parameters (?temp ?suit -sensor ?f -actuator)
        :precondition (and (not(TempHigh ?temp)) (FanOn ?f) (not(TempSuitable ?suit)))
        :effect (and (not(FanOn ?f)) (TempSuitable ?suit))
    )

    
    (:action SpotOccupied
        :parameters (?ultra ?spotstatus -sensor  ?spotled -actuator)
        :precondition (and (not(UltrasonicHigh ?ultra)) (not(Suitable ?spotstatus)) (LedOn ?spotled) )
        :effect (and (not(LedOn ?spotled)) (Suitable ?spotstatus))
    )
    (:action SpotNotOccupied
        :parameters (?ultra ?spotstatus -sensor  ?spotled -actuator)
        :precondition (and (UltrasonicHigh ?ultra) (not(LedOn ?spotled))(not(suitable ?spotstatus)))
        :effect (and (LedOn ?spotled)(Suitable ?spotstatus))
    )
)