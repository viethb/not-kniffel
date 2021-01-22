{
    "use strict";

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const ids = ['first', 'second', 'third', 'fourth', 'fifth'];
    const names = ['keep_1', 'keep_2', 'keep_3', 'keep_4', 'keep_5']
    function checkChecked(name, id){
        if (urlParams.has(name)) {
            try {
              document.getElementById(id).checked = true;
            }
            catch (err){}
        }
    }

    for (let i = 0; i < ids.length; i++){
        checkChecked(names[i], ids[i]);
    }
}