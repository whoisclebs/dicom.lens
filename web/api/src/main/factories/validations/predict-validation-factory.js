import { ValidationComposite } from "../../../validation/index.js"
import { RequiredFieldValidation } from "../../../validation/validators/field-required-validation.js"

export const makePredictValidation = () => {
    const validations = []
    for (const field of ['img']) {
      validations.push(new RequiredFieldValidation(field))
    }
    return new ValidationComposite(validations)
}