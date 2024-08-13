import * as dashboard from "./dashboard.js";
import * as views from "../views/library.js";
import {get_all_storage} from "../models/storage.js";


document.addEventListener("DOMContentLoaded", async () => {
    const storage = await get_all_storage();
    views.render_library(storage);
})

