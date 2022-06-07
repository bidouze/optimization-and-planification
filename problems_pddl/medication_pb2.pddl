(define (problem pb2)
  (:domain transport_pharmacie)
  (:objects
    t1 t2 t3   - truck
    l1 l2 l3 l4 l5 l6 - location
    c1 c2 c3 c4 c5 c6 c7 - container
    m1 m2 m3 m4 m5 - medication
  )
  (:init
    (linked l2 l3) (linked l3 l2)
    (linked l1 l2) (linked l2 l1)
    (linked l2 l4) (linked l4 l2)
    (linked l4 l5) (linked l5 l4)
    (linked l3 l6) (linked l6 l3)
    (include c1 t1)
    (include c2 t1)
    (include c3 t2)
    (include c4 t2)
    (include c5 t2)
    (include c6 t1)
    (include c7 t1)
    (at t1 l1)
    (at t2 l6)
    (at t3 at l4)
    (free c1)
    (free c2)
    (free c3)
    (free c4)
    (free c5)
    (free c6)
    (free c7)
    (stocked l2 m1)
    (stocked l3 m2)
    (stocked l6 m3)
    (stocked l5 m4)
    (stocked l5 m5)

  )
  ; the task is to stock location 1 with all medications
  (:goal (and (stocked l1 m1) (stocked l1 m2) (stocked l1 m3) (stocked l1 m4) (stocked l1 m5) ))
)
