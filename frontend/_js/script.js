function mascara_cpf(i){
   
    var v = i.value;
    
    if(isNaN(v[v.length-1])){ // impede entrar outro caractere que não seja número
        i.value = v.substring(0, v.length-1);
        return;
    }
    
    i.setAttribute("maxlength", "14");
    if (v.length == 3 || v.length == 7) i.value += ".";
    if (v.length == 11) i.value += "-";

}

function testa_cpf(campo_cpf){
    valor_do_campo = campo_cpf.value
    cpf = valor_do_campo.replace(/[.-]/g,'')
    
    soma1 = 0
    for(i = 0; i < 9; i++){
        soma1 += cpf[i] * (10-i)
    }
    resto1 = ((soma1 * 10) % 11)%10

    soma2 = 0
    for(i = 0; i < 10; i++){
        soma2 += cpf[i] * (11-i)
    }
    resto2 = ((soma2 * 10) % 11)%10

    valido = true

    if(resto1 == cpf[9] & resto2 == cpf[10]){
        valido = true
    }
    else{
        valido = false
    }
    if(/^(.)\1*$/.test(cpf)){
        valido = false
    }

    if(!valido){
        $("#cpf").css("border", "1px solid red")
        console.log(soma1, resto1, soma2, resto2, valido, /^(.)\1*$/.test(cpf))
    }
    else{
        $("#cpf").css("border", "1px solid #ced4da")
    }

};
String.prototype.formatUnicorn = String.prototype.formatUnicorn ||
function () {
    "use strict";
    var str = this.toString();
    if (arguments.length) {
        var t = typeof arguments[0];
        var key;
        var args = ("string" === t || "number" === t) ?
            Array.prototype.slice.call(arguments)
            : arguments[0];

        for (key in args) {
            str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
        }
    }

    return str;
};
