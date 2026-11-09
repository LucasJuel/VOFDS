MARB_TB := course-material/DTU-2026-02207/assignment/marb/src/tb

.PHONY: sim clean coverage

sim:
	$(MAKE) -C $(MARB_TB)

clean:
	$(MAKE) -C $(MARB_TB) clean

coverage:
	$(MAKE) -C $(MARB_TB) coverage

# Pass any other target through to the assignment Makefile
%:
	$(MAKE) -C $(MARB_TB) $@
