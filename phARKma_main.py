import trial_updater
import get_company_data
import phARKma_utils
import get_relationships
import get_trials
import trial_updater
import airtable_utils
import get_condition_category
import get_arkg_tickers
import get_details
import get_commercialized_drugs



tickers = get_arkg_tickers.get_arkg_tickers()

trials_database = phARKma_utils.get_trials_database()
for ticker in tickers[3:]:
    trials = get_trials.get_trials_primary(ticker, trials_database)
    # collab_trials = get_trials.get_trials_collaborator(ticker, trials_database)
    for trial in trials:
        airtable_utils.add_clinical_trial("Clinical Trials",trial, ticker)
    # for trial in collab_trials:
    #     airtable_utils.add_clinical_trial("Clinical Trials",trial, ticker)

airtable_utils.remove_duplicate_records("Clinical Trials")

    