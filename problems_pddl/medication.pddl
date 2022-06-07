(define (domain transport_pharmacie)
  (:requirements :strips :typing :negative-preconditions)

  (:types
    locations  ; there are several providers of medications and pharmacies
    truck  ; hold "X" containers
    containers; container can contain one medication each and they are always in a truck
    medication
  )

  (:predicates
    (at ?t - truck ?l - location)       ; truck ?t is at location ?l
    (free ?c - container )              ; container ?c is empty
    (stocked ?l - location  ?m - medication)      ; location ?l is stocked with medication ?m
    (in ?m - medication ?c - container) ; medication ?m is in container ?c
    (include ?c - container ?t - truck)      ; container ?c is in truck ?t
    (linked ?l1 -location1 ?l2 - location2); location 1 has a direct road to location 2 
    (equal ?m1 ?m2)                     ; medication ?m1 is equal to ?m2

  )

  ; load container of a truck with medication at a certain location
  (:action load
    :parameters (?m - medication ?l - location ?t - truck ?c - container)
    :precondition (and (free ?c) (at ?t ?l) (stocked ?l ?m) (include ?c ?t))
    :effect (and (in ?m ?c) (not (stocked ?l ?m)) (not (free ?c)))
  )

  ; unload container of a truck with medication at a certain location
  (:action unload
    :parameters (?m - medication ?l - location ?t - truck ?c - container)
    :precondition (and (in ?m ?c) (at ?t ?l) (not (stocked  ?l ?m)) (not (free ?c)) (include ?c ?t))
    :effect (and (free ?c) (not (in ?m ?c)) (stocked ?l ?m))
  )

  ; move truck from one location to the other
  (:action move
    :parameters (?t - truck ?l1 - location ?l2 - location)
    :precondition (and (linked ?l1 ?l2) (at ?t ?l1))
    :effect (and (at ?t ?l2) (not(at ?t ?l1)))
  )

)




