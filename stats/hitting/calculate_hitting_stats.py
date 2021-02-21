from stats.hitting.hitting_factors import get_factors
from util.number_utils import min_max
from output_utils.progress.progress_bar import ProgressBar

def calculate_hitting_stats(cards, vl_data, vr_data, ovr_woba_factors, vl_woba_factors, vr_woba_factors):
    hitting_factors = get_factors(vl_data, vr_data)

    # TODO calculate in ovr_data keys when used.
    progress_bar = ProgressBar(len(cards), "Calculate batting projections")
    for card in cards:
        factors = hitting_factors["VL"][card["bats"]]
        _set_projections(card, factors, vl_woba_factors, "vL")

        factors = hitting_factors["VR"][card["bats"]]
        _set_projections(card, factors, vr_woba_factors, "vR")

        progress_bar.increment()

    progress_bar.finish()
    print()

def _set_projections(card, factors, woba_factors, mod):
    # TODO will talk about HBP data later
    tot_pas = 720
    hbp = 3
    bb = min_max(0, factors["eye"](card) * (tot_pas - hbp), tot_pas - hbp)
    k = min_max(0, factors["avk"](card) * (tot_pas - bb - hbp), tot_pas - bb - hbp)
    hr = min_max(0, factors["pow"](card) * (tot_pas - bb - k - hbp), tot_pas - bb - k - hbp)
    hits = min_max(0, factors["babip"](card) * (tot_pas - bb - k - hr - hbp), tot_pas - bb - k - hr - hbp)
    xbh = min_max(0, factors["gap"](card) * hits, hits)
    triples = min_max(0, factors["spe"](card) * xbh, xbh)
    doubles = xbh - triples
    singles = hits - xbh
    avg = (hits + hr) / (tot_pas - bb - hbp)
    obp = (hits + hr + bb + hbp) / tot_pas
    ops = obp + (singles + doubles * 2 + triples * 3 + hr * 4) / (tot_pas - hbp - bb)
    woba = (
        woba_factors["hbp_factor"] * hbp 
            + woba_factors["walks_factor"] * bb 
            + woba_factors["singles_factor"] * singles 
            + woba_factors["doubles_factor"] * doubles 
            + woba_factors["triples_factor"] * triples 
            + woba_factors["homeruns_factor"] * hr
        ) / tot_pas

    card["HBP_" + mod] = 3
    card["BB_" + mod] = bb
    card["K_" + mod] = k
    card["HR_" + mod] = hr
    card["singles_" + mod] = singles
    card["doubles_" + mod] = doubles
    card["triples_" + mod] = triples
    card["AVG_" + mod] = avg
    card["OBP_" + mod] = obp
    card["OPS_" + mod] = ops
    card["wOBA_" + mod] = woba