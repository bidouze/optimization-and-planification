(define (problem pb1)
  (:domain transport_pharmacie)
  (:objects
    t1    - truck
    l1 l2 l3 - location
    c1    - container
    m1 m2 - medication
  )
  (:init
    (linked l2 l3) (linked l3 l2)
    (linked l1 l2) (linked l2 l1)
    (include c1 t1)
    (at t1 l1)
    (free c1)
    (stocked l2 m1)
    (stocked l3 m2)

  )
  ; the task is to stock location 1 with both medications
  (:goal (and (stocked l1 m1) (stocked l1 m2) ))
)


