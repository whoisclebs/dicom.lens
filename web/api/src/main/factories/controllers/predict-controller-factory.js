import { PredicController } from "../../../presentation/controllers/predict-controller.js"
import { makeModel } from "../usecases/model-factory.js"
import { makePredictValidation } from "../validations/predict-validation-factory.js"

export const makePredictController = () => {
  const controller = new PredicController(makeModel(), makePredictValidation())
  return controller;
}