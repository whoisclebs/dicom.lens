import { adaptRoute } from "../adapters/route-adapter.js"
import { makePredictController } from "../factories/controllers/predict-controller-factory.js"

export default (router) => {
    router.post('/ml/predict', adaptRoute(makePredictController()))
}