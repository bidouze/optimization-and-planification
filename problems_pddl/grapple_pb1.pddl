(define (problem pb1)
  (:domain grapple)
    (:objects
    1 2 3 4 5 6 7 - location
    a b c d e - container
  )
  (:init (freegrapple) (left 1 2) (left 2 3) (left 3 4) (left 4 5) (left 5 6) (left 6 7) (is a 1) (is b 2) (is c 3) (is d 4) (is e 5) (free 6) (free 7))
  (:goal (and (is a 5) (is b 3) (is c 2) (is d 4) (is e 1))))
