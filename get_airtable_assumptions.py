import airtable_utils


def get_sales_curve():
    sc_records = airtable_utils.get_airtable_records("Sales Curve")
    sales_curve_dict = {}
    for entry in sc_records:
        sales_curve_dict[entry["fields"]["YEAR"]] = str(entry["fields"]["PERCENT_PEAK_SALES"])
    
    return sales_curve_dict

def get_area_specific_time_coefficients():
    astc_records = airtable_utils.get_airtable_records("Area-Specific Time Coefficients")
    astc_dict = {}
    for entry in astc_records:
        astc_dict[entry["fields"]["AREA"]] = str(entry["fields"]["RND_TIME_COEFFICIENT"])
    
    return astc_dict

def get_area_specific_peak_sales_coefficients():
    aspsc_records = airtable_utils.get_airtable_records("Area-Specific Peak Sales Coefficients")
    aspsc_dict = {}
    for entry in aspsc_records:
        aspsc_dict[entry["fields"]["AREA"]] = str(entry["fields"]["PEAK_SALES_COEFFICIENT"])
    
    return aspsc_dict

def get_percent_rnd_spend_by_phase():
    prndbp_records = airtable_utils.get_airtable_records("R&D Spend by Phase")
    prndbp_dict = {}
    for entry in prndbp_records:
        prndbp_dict[entry["fields"]["PHASE"]] = str(entry["fields"]["PERCENT_SPEND"])
    
    return prndbp_dict

def get_phase_discount_rates():
    pdr_records = airtable_utils.get_airtable_records("Phase Discount Rates")
    pdr_dict = {}
    for entry in pdr_records:
        pdr_dict[entry["fields"]["PHASE"]] = str(entry["fields"]["DISCOUNT_RATE"])
    
    return pdr_dict

def get_phase_cost_per_drug():
    pcpd_records = airtable_utils.get_airtable_records("Phase Cost Per Drug")
    pcpdr_dict = {}
    for entry in pcpd_records:
        pcpdr_dict[entry["fields"]["PHASE"]] = str(entry["fields"]["COST"])
    
    return pcpdr_dict

def get_phase_transition_probabilities():
    ptp_records = airtable_utils.get_airtable_records("Phase Transition Probabilities")
    ptp_dict = {}
    for entry in ptp_records:
        ptp_dict[entry["fields"]["START_PHASE"]] = str(entry["fields"]["PROBABILITY"])
    
    return ptp_dict

def get_net_margin():
    oa_records = airtable_utils.get_airtable_records("Other Assumptions")
    net_margin = None
    for entry in oa_records:
        if entry["fields"]["ASSUMPTION"] == "NET_MARGIN":
            net_margin = entry["fields"]["VALUE"]
    
    return float(net_margin)

def get_risk_free_rate():
    oa_records = airtable_utils.get_airtable_records("Other Assumptions")
    rfr = None
    for entry in oa_records:
        if entry["fields"]["ASSUMPTION"] == "RISK_FREE_RATE":
            rfr = entry["fields"]["VALUE"]

    return float(rfr)

def get_corporate_tax_rate():
    oa_records = airtable_utils.get_airtable_records("Other Assumptions")
    ctr = None
    for entry in oa_records:
        if entry["fields"]["ASSUMPTION"] == "CORPORATE_TAX":
            ctr = entry["fields"]["VALUE"]

    return float(ctr)

def get_tax_break():
    oa_records = airtable_utils.get_airtable_records("Other Assumptions")
    tb = None
    for entry in oa_records:
        if entry["fields"]["ASSUMPTION"] == "TAX_BREAK":
            tb = entry["fields"]["VALUE"]

    return float(tb)

def get_rnd_cost_of_capital():
    oa_records = airtable_utils.get_airtable_records("Other Assumptions")
    rndcoc = None
    for entry in oa_records:
        if entry["fields"]["ASSUMPTION"] == "RND_COST_OF_CAPITAL":
            rndcoc = entry["fields"]["VALUE"]

    return float(rndcoc)




