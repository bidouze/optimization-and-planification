(define (problem pb2)
  (:domain grapple)
    (:objects
    1 2 3 4 5 6 7 8 9  - location
    a b c d e f  - container
  )
  (:init (freegrapple) (left 1 2) (left 2 3) (left 3 4) (left 4 5) (left 5 6)
   (left 6 7) (left 7 8) (left 8 9)
  (is a 1) (is b 2) (is c 3) (is d 4) (is e 5)  (is f 6)
  (free 8) (free 9) )
  (:goal (and (is a 6) (is b 4) (is c 1) (is d 5) (is e 3)  (is f 2))))
