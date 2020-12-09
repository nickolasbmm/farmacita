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
        $("#cpf").val("")
        selectCPF.placeholder="CPF inválido"
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
adiciona_sugestao_generic = function(sugestoes, datalist_id){
    $("#" + datalist_id).empty()
    sugestoes.forEach(sugestao=> {
        $("#" + datalist_id).append(
            '<option value="{valor}"">'.formatUnicorn({valor : sugestao})
                )
    });
}

remove_parent = function (item){ 
    item.parentNode.parentNode.removeChild(item.parentNode)
}


function validarCNPJ(cnpj) {
    valor_do_campo = cnpj.value
    cnpj = valor_do_campo.replace(/[^\d]+/g,'');
    valido = true;
    if(cnpj == '') return false;
     
    if (cnpj.length != 14)
        valido = false;
 
    // Elimina CNPJs invalidos conhecidos
    if (cnpj == "00000000000000" || 
        cnpj == "11111111111111" || 
        cnpj == "22222222222222" || 
        cnpj == "33333333333333" || 
        cnpj == "44444444444444" || 
        cnpj == "55555555555555" || 
        cnpj == "66666666666666" || 
        cnpj == "77777777777777" || 
        cnpj == "88888888888888" || 
        cnpj == "99999999999999")
        valido = false;
         
    // Valida DVs
    tamanho = cnpj.length - 2
    numeros = cnpj.substring(0,tamanho);
    digitos = cnpj.substring(tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0))
        valido = false;
         
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0,tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1))
        valido = false;
           
    
    if(!valido){
        $("#cnpj").css("border", "1px solid red")
        console.log(soma1, resto1, soma2, resto2, valido, /^(.)\1*$/.test(cnpj))
    }
    else{
        $("#cnpj").css("border", "1px solid #ced4da")
    }
    
    
}