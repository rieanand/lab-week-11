.PHONY: environment environment-bonus remove-env remove-env-bonus

ENVIRONMENT=chem274A_ssn
BONUS_ENVIRONMENT=chem274A_ssn_bonus

environment:
	conda env create -f environment.yml -n $(ENVIRONMENT)

environment-bonus:
	conda env create -f environment-bonus.yml -n $(BONUS_ENVIRONMENT)

remove-env:
	conda remove --name $(ENVIRONMENT) --all --yes

remove-env-bonus:
	conda remove --name $(BONUS_ENVIRONMENT) --all --yes
