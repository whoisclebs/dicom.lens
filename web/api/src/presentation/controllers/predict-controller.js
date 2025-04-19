import { badRequest, serverError, ok } from '../helpers/index.js'

export class PredicController {
  constructor (
    model,
    validation
  ) {
    this.model = model
    this.validation = validation
  }

  async handle (request) {
    try {
      const error = this.validation.validate(request)
      if (error) {
        return badRequest(error)
      }
      const prediction = await this.model.predict(request)
      return ok(prediction)
    } catch (error) {
      return serverError(error)
    }
  }
}