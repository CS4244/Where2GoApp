;;question refers to the question to be asked
;; choice refers to the choices available to the user
;;slotName refers to the actual slot name in the desired template
;;For questionType, radio implies question accepts only one answer and checkbox accepts multiple answers. 
(deftemplate ask
	(slot question (type STRING))
	(multislot choice (type STRING))
	(slot slotName (type STRING))
  (slot questionType (type STRING) (allowed-strings "RADIO" "CHECKBOX") (default "RADIO"))
	)

(deftemplate destination
	(slot name (type STRING))
	(slot climate (type STRING) (allowed-strings "summer" "winter" "autumn" "spring"))
	(slot visitMth(type INTEGER) (range 1 12))
	(slot englishSpeaking (type STRING) (default "no")(allowed-strings "yes" "no"))
	(slot visitPurpose (type STRING)(allowed-strings "adventure" "pleasure"))
	(slot region (type STRING))
	(slot budget (type INTEGER))
	(slot activityType (type STRING))
	(slot indoorActivity (type STRING)(default "no")(allowed-strings "yes" "no"))
	(slot outdoorActivity (type STRING)(default "no")(allowed-strings "yes" "no"))
	(slot safety (type STRING)(default "no")))

(deftemplate MAIN::attribute   
	(slot name)   
	(slot value))

(deftemplate desired
	; ;(slot name (type STRING))
	(slot englishSpeaking (type STRING) (default "NULL")(allowed-strings "NULL" "Yes" "No"))
	(multislot visitPreference (type STRING) (default "NULL") (allowed-strings "NULL" "Off the Beaten Path" "Romantic" "Peace and Quiet" "Local Culture" "Nightlife" "Family Friendly" "Leisure"))
	(slot region (type STRING)(allowed-strings "NULL" "North America" "Europe" "Other"))
	(multislot geography (type STRING) (default "NULL") (allowed-strings "NULL" "Beach" "City" "Volcano" "Coastal" "Mountains" "Forest" "Island"))
	(multislot leisure (type STRING) (default "NULL") (allowed-strings "NULL" "Casino" "Spa" "Shopping" "Theme Park" "Landmarks" "Zoo" "Museum" "Dining"))
	(slot daysReq (type INTEGER))
	(slot budget (type INTEGER))
	(multislot activityType (type STRING) (default "NULL") (allowed-strings "NULL" "Water" "Outdoor"))
	(multislot waterActivity (type STRING) (default "NULL") (allowed-strings "NULL" "Surfing" "Snorkelling" "Water Skiing" "Water Park" "Wind Surfing" "Dolphin Encounter"))
	(multislot outdoorActivity (type STRING) (default "NULL") (allowed-strings "NULL" "Mountain Biking" "Rock Climbing" "Hiking" "Snow Skiing" "Zip Line" "Horseback Riding"))
	(slot weather (type STRING) (allowed-strings "NULL" "Hot" "Warm" "Mild" "Cold" "Frozen"))
)


(defrule MAIN::start  
(attribute (name budget) (value ?))
=>  
(assert (done)))
(deffacts the-facts
	(desired)
	
)

(defrule fireWeatherQuestion
?desired <- (desired (weather "NULL"))
=>
(assert (ask (question "What is your ideal weather") (choice "hot" "warm" "mild" "cold") (slotName "weather")))
)

(defrule fireEnglishSpeakingQuestion
?desired <- (desired (englishSpeaking "NULL"))
=>
(assert (ask (question "Do you prefer your destination to be an English-speaking destination?") (choice "Yes" "No") (slotName "englishSpeaking")))
)

(defrule fireRegionQuestion
?desired <- (desired (region "NULL"))
=>
(assert (ask (question "What is your ideal destination region?") (choice "North America" "Europe" "Other") (slotName "region")))
)

(defrule fireActivityTypeQuestion
?desired <- (desired (activityType "NULL"))
=>
(assert (ask (question "What kind of activities do you wish to take part in?") (choice "Outdoor" "Water") (slotName "activityType") (questionType "CHECKBOX")))
)


(defrule firehaha
?desired <- (desired (englishSpeaking "Yes"))
=>
(assert (we won))
)

; ; Fire english speaking destination preference question
(defrule fireEnglishSpeakingQuestion1
?desired <- (desired (englishSpeaking "NULL"))
=>
(printout t "Do you prefer your destination to be an English-speaking destination? (1.Yes; 2.No) ")
(bind ?n (read))
(switch ?n 
	(case 1 then (modify ?desired (englishSpeaking "Yes")))
	(case 2 then (modify ?desired (englishSpeaking "No")))
)
)