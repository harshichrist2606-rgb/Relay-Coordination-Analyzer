import math


def relay_operating_time(fault_current, pickup_current, tms):
    """
    IEC Standard Inverse overcurrent relay characteristic.

    t = TMS * 0.14 / ((I/Is)^0.02 - 1)
    """

    current_multiple = fault_current / pickup_current

    if current_multiple <= 1:
        return None

    operating_time = (
        tms * 0.14
        / (math.pow(current_multiple, 0.02) - 1)
    )

    return operating_time


def relay_coordination_analyzer():

    print("=" * 70)
    print("              RELAY COORDINATION ANALYZER")
    print("=" * 70)

    # --------------------------------------------------
    # PRIMARY RELAY
    # --------------------------------------------------

    print("\nPRIMARY RELAY SETTINGS")

    primary_pickup = float(
        input("Enter primary relay pickup current (A): ")
    )

    primary_tms = float(
        input("Enter primary relay TMS: ")
    )

    # --------------------------------------------------
    # BACKUP RELAY
    # --------------------------------------------------

    print("\nBACKUP RELAY SETTINGS")

    backup_pickup = float(
        input("Enter backup relay pickup current (A): ")
    )

    backup_tms = float(
        input("Enter backup relay TMS: ")
    )

    # --------------------------------------------------
    # FAULT AND COORDINATION SETTINGS
    # --------------------------------------------------

    print("\nFAULT AND COORDINATION DATA")

    fault_current = float(
        input("Enter fault current (A): ")
    )

    required_cti = float(
        input("Enter required coordination interval (s): ")
    )

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    if primary_pickup <= 0 or backup_pickup <= 0:
        print("Pickup currents must be greater than zero.")
        return

    if primary_tms <= 0 or backup_tms <= 0:
        print("TMS values must be greater than zero.")
        return

    if fault_current <= 0:
        print("Fault current must be greater than zero.")
        return

    if required_cti < 0:
        print("Required CTI cannot be negative.")
        return

    # --------------------------------------------------
    # CURRENT MULTIPLES
    # --------------------------------------------------

    primary_multiple = fault_current / primary_pickup
    backup_multiple = fault_current / backup_pickup

    print("\n" + "-" * 70)
    print("CURRENT MULTIPLES")
    print("-" * 70)

    print(
        f"Primary Relay Current Multiple : "
        f"{primary_multiple:.3f} ×"
    )

    print(
        f"Backup Relay Current Multiple  : "
        f"{backup_multiple:.3f} ×"
    )

    # --------------------------------------------------
    # OPERATING TIMES
    # --------------------------------------------------

    primary_time = relay_operating_time(
        fault_current,
        primary_pickup,
        primary_tms
    )

    backup_time = relay_operating_time(
        fault_current,
        backup_pickup,
        backup_tms
    )

    print("\n" + "-" * 70)
    print("RELAY OPERATING TIMES")
    print("-" * 70)

    if primary_time is None:
        print("Primary relay: FAULT CURRENT BELOW PICKUP")
        return

    if backup_time is None:
        print("Backup relay: FAULT CURRENT BELOW PICKUP")
        return

    print(
        f"Primary Relay Operating Time : "
        f"{primary_time:.4f} s"
    )

    print(
        f"Backup Relay Operating Time  : "
        f"{backup_time:.4f} s"
    )

    # --------------------------------------------------
    # COORDINATION
    # --------------------------------------------------

    cti = backup_time - primary_time

    print("\n" + "-" * 70)
    print("COORDINATION ANALYSIS")
    print("-" * 70)

    print(f"Required CTI : {required_cti:.4f} s")
    print(f"Actual CTI   : {cti:.4f} s")

    if cti >= required_cti:
        coordination_status = "SATISFACTORY"
    else:
        coordination_status = "UNSATISFACTORY"

    # Check relay sequence
    if primary_time < backup_time:
        sequence_status = "CORRECT"
    else:
        sequence_status = "INCORRECT"

    print(f"Trip Sequence : {sequence_status}")
    print(f"Coordination  : {coordination_status}")

    # --------------------------------------------------
    # FINAL PROTECTION DECISION
    # --------------------------------------------------

    print("\n" + "-" * 70)
    print("PROTECTION ASSESSMENT")
    print("-" * 70)

    if (
        sequence_status == "CORRECT"
        and coordination_status == "SATISFACTORY"
    ):
        print("✓ PRIMARY-BACKUP COORDINATION IS SATISFACTORY")
        print("✓ Primary relay operates first.")
        print("✓ Backup relay provides delayed backup protection.")
    else:
        print("✗ RELAY COORDINATION IS NOT SATISFACTORY")

        if sequence_status != "CORRECT":
            print(
                "  - Backup relay may operate before "
                "the primary relay."
            )

        if coordination_status != "SATISFACTORY":
            print(
                "  - Coordination time interval is "
                "insufficient."
            )

    print("\n" + "=" * 70)
    print("Relay coordination analysis completed.")
    print("=" * 70)


if __name__ == "__main__":
    relay_coordination_analyzer()
