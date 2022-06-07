(define (domain grapple)
  (:requirements :strips :negative-preconditions)

    (:types
    location
    container
  )

  (:predicates
  (is ?A - container ?i - location)
  (taken ?A - container)
  (takenright ?A - container)
  (takenleft ?A - container)
  (left ?i - location ?j - location)
  (free  ?i - location)
  (freegrapple)
  )

  (:action take1
    :parameters (?A - container ?i - location)
    :precondition (and (is ?A ?i) (freegrapple))
    :effect (and (not (is ?A ?i)) (free ?i) (taken ?A) (not (freegrapple)))
  )

  (:action take2
    :parameters (?A - container ?i - location ?B - container ?j - location)
    :precondition (and (is ?A ?i) (is ?B ?j) (left ?i ?j) (freegrapple))
    :effect (and (not (is ?A ?i)) (free ?i) (takenleft ?A) (not (is ?B ?j)) (free ?j) (takenright ?B) (not (freegrapple)))
  )

  (:action putdown1
    :parameters (?A - container ?i - location)
    :precondition (and (taken ?A) (free ?i))
    :effect (and (is ?A ?i) (not (free ?i)) (not (taken ?A)) (freegrapple))
  )

  (:action putdown2
    :parameters (?A - container ?i - location ?B - container ?j - location)
    :precondition (and (takenleft ?A) (free ?i) (takenright ?B) (free ?j) (left ?i ?j) )
    :effect (and (is ?A ?i) (not(free ?i)) (not(takenleft ?A)) (is ?B ?j) (not(free ?j)) (not(takenright ?B)) (freegrapple))
  )
)
