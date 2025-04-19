import { MissingParamError } from "../../presentation/errors/missing-param-error.js"

export class RequiredFieldValidation {
  constructor (fieldName) {
    this.fieldName = fieldName
  }
  
  validate (input) {
    if (!input[this.fieldName]) {
        return new MissingParamError(this.fieldName)
    }
  }
}