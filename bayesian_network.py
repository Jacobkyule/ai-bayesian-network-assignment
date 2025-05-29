from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def build_model():
    # Define the network structure
    model = DiscreteBayesianNetwork([
        ('Disease', 'TestResult'),
        ('Disease', 'Symptom1'),
        ('Disease', 'Symptom2')
    ])

    # Define CPDs
    cpd_disease = TabularCPD(variable='Disease', variable_card=2, values=[[0.99], [0.01]])

    cpd_symptom1 = TabularCPD(variable='Symptom1', variable_card=2,
                              values=[[0.9, 0.2],  # Symptom1=False
                                      [0.1, 0.8]], # Symptom1=True
                              evidence=['Disease'],
                              evidence_card=[2])

    cpd_symptom2 = TabularCPD(variable='Symptom2', variable_card=2,
                              values=[[0.95, 0.3],
                                      [0.05, 0.7]],
                              evidence=['Disease'],
                              evidence_card=[2])

    cpd_test = TabularCPD(variable='TestResult', variable_card=2,
                          values=[[0.8, 0.1],
                                  [0.2, 0.9]],
                          evidence=['Disease'],
                          evidence_card=[2])

    # Add CPDs to the model
    model.add_cpds(cpd_disease, cpd_symptom1, cpd_symptom2, cpd_test)

    # Verify model correctness
    if not model.check_model():
        raise ValueError("Model is incorrect")

    return model

def perform_inference(model, evidence):
    inference = VariableElimination(model)
    posterior = inference.query(variables=['Disease'], evidence=evidence)
    return posterior

if __name__ == "__main__":
    model = build_model()

    # Example evidence where Symptom1=True, Symptom2=True, TestResult=Positive
    evidence = {'Symptom1': 1, 'Symptom2': 1, 'TestResult': 1}

    result = perform_inference(model, evidence)
    print("Posterior probability of Disease given evidence:")
    print(result)
