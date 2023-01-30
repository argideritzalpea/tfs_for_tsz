;;;
;;; this file should be `Index.lisp' and reside in the directory containing the
;;; tsdb(1) test suite skeleton databases (typically a subdirectory `skeletons'
;;; in the tsdb(1) database root directory `*tsdb-home*').
;;;
;;; the file should contain a single un-quote()d Common-Lisp list enumerating
;;; the available skeletons, e.g.
;;;
;;;   (((:path . "english") (:content . "English TSNLP test suite"))
;;;    ((:path . "csli") (:content . "CSLI (ERGO) test suite"))
;;;    ((:path . "vm") (:content . "English VerbMobil data")))
;;;
;;; where the individual entries are assoc() lists with at least two elements:
;;;
;;;   - :path --- the (relative) directory name containing the skeleton;
;;;   - :content --- a descriptive comment.
;;;
;;; the order of entries is irrelevant as the `tsdb :skeletons' command sorts
;;; the list lexicographically before output.
;;;

(
((:path . "matrix") (:content . "matrix: A test suite created automatically from the test sentences given in the Grammar Matrix questionnaire."))
((:path . "corpus") (:content . "IGT provided by the linguist"))
((:path . "lab4") (:content . "Lab 4"))
((:path . "lab3") (:content . "Lab 3"))
((:path . "lab2") (:content . "IGT provided by the linguist"))
;((:path . "after_lab2") (:content . "IGT provided by the linguist"))
; New test suites here. For example:
; ((:path . "new-test-suite") (:content . "New Test Suite: A description of the new test suite located at the subdirectory new-test-suite."))
)
