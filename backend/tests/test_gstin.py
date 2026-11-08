import pytest
import random
from sqlmodel import Session, select
from backend.app.db import engine
from backend.app.models import RegistryGSTIN
from backend.app.services.gstin import (
    check_gstin_format,
    check_gstin_checksum,
    lookup_gstin,
    CHARSET
)

def test_all_registry_gstins_pass_format_and_checksum():
    with Session(engine) as session:
        gstins = session.exec(select(RegistryGSTIN.gstin)).all()
        assert len(gstins) == 3534, f"Expected 3534 GSTINs, found {len(gstins)}"
        
        failed = []
        for g in gstins:
            if not check_gstin_format(g):
                failed.append((g, "format"))
            elif not check_gstin_checksum(g):
                failed.append((g, "checksum"))
                
        assert len(failed) == 0, f"Failed GSTINs: {failed[:10]}"


def test_20_mutated_gstins_fail():
    with Session(engine) as session:
        all_gstins = session.exec(select(RegistryGSTIN.gstin)).all()
        # Sample 20 GSTINs
        random.seed(42)
        sample = random.sample(all_gstins, 20)
        
        for g in sample:
            # Mutate one char (not the 15th, or change the 15th to a wrong check char)
            idx = random.randint(0, 13)
            orig_char = g[idx]
            # Pick a different char
            other_chars = [c for c in CHARSET if c != orig_char]
            mutated = g[:idx] + random.choice(other_chars) + g[idx+1:]
            
            # Format might pass, but checksum MUST fail
            # (unless accidental collision on mod 36, which is 1/36, so if it happens mutate check digit)
            if check_gstin_checksum(mutated):
                # If checksum happened to match, mutate the 15th character
                cur_15 = mutated[14]
                new_15 = [c for c in CHARSET if c != cur_15][0]
                mutated = mutated[:14] + new_15
                
            assert check_gstin_checksum(mutated) is False, f"Mutated GSTIN {mutated} unexpectedly passed checksum!"
