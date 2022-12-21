import { Streamlit, RenderData } from "streamlit-component-lib"
import Cookies from "js-cookie"


function isAllowed(str) {
  if (typeof(str) == "string") {
    if (str == "") return false;
    var regu = "^[ ]+$";
    var re = new RegExp(regu);
    return !re.test(str);
  } else {
    return false;
  }
}


function onRender(event: Event): void {
  const data = (event as CustomEvent<RenderData>).detail
  let act = data.args["act"]
  let name = data.args["name"]
  if (isAllowed(name) == false) {
    return Streamlit.setComponentValue({"code": "-1", "msg": "Name not allowed!"})
  }
  if (isAllowed(act) == false) {
    return Streamlit.setComponentValue({"code": "-1", "msg": "Action not specified!"})
  }
  if (act == "del") {
    Cookies.remove(name)
    Streamlit.setComponentValue({"code": "200", "msg": "Deletion succeeded!"})
  }
  else if (act == "add") {
    let value = data.args["value"]
    Cookies.set(name, value, { expires: 36500 })
    Streamlit.setComponentValue({"code": "200", "msg": "Addition succeeded!"})
  }
  else if (act == "get") {
    let value = Cookies.get(name) || null
    Streamlit.setComponentValue({"code": "200", "msg": "Query succeeded!", "value": value})
  }
  else {
    Streamlit.setComponentValue("Action not allowed!")
  }
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
