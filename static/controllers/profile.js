import * as dashboard from "./dashboard.js";
import * as models from "../models/user.js";
import * as views from "../views/profile.js"

 document.addEventListener("DOMContentLoaded", async () => {
   const profile = await models.fetch_user_profile();
   await views.render_profile(profile);
 });