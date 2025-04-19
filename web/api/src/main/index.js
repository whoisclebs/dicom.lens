import env from './factories/env.js'
import { makeApp } from './factories/app.js'

makeApp().then(app => {
  app.listen(env.port, () => {
    console.log(`Server running at http://localhost:${env.port}`)
  })
})