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
    valido = false
    if (cpf.length == 11){
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
    }
    if(!valido){
        selectCPF = $("#cpf")[0]
        $("#cpf").val("")
        selectCPF.placeholder="CPF inválido"
        $("#cpf").css("border", "1px solid red")
        console.log(soma1, resto1, soma2, resto2, valido, /^(.)\1*$/.test(cpf))
    }
    else{
        $("#cpf").css("border", "1px solid #ced4da")
    }

};
validarCNPJ = (campo_cnpj) =>{
    cnpj = campo_cnpj.value.replace(/\D/g,"")
    valid = false
    console.log(cnpj.length)
    if(cnpj.length == 14){
        array_validacao1 = [5,4,3,2,9,8,7,6,5,4,3,2]
        sum1 = 0
        for (i = 0; i < array_validacao1.length; i++){
            sum1 += cnpj[i] * array_validacao1[i]
        }
        resto1 = sum1%11
        if (resto1 < 2){
            resto1 = 0
        }else{
            resto1 = 11 - resto1
        }

        array_validacao2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
        sum2 = 0
        for (i = 0; i < array_validacao2.length; i++){
            sum2 += cnpj[i] * array_validacao2[i]
        }
        resto2 = sum2%11
        if (resto2 < 2){
            resto2 = 0
        }else{
            resto2 = 11 - resto2
        }
        console.log(resto1, cnpj[12], resto2, cnpj[13])
        if (resto1 == cnpj[12] && resto2 == cnpj[13]){
            valid = true
        }
    }

    if(!valid){
        selectCNPJ = $("#cnpj")[0]
        $("#cnpj").val("")
        selectCNPJ.placeholder="cnpj inválido"
        $("#cnpj").css("border", "1px solid red")
    }
    else{
        $("#cnpj").css("border", "1px solid #ced4da")
    }
    
}

function confirmar_senha(campo_senha){
    campo = campo_senha.value
    if($("#senha").val()==campo){
        $("#confirmacao_senha").css("border", "1px solid #ced4da")
        $("#texto_confirmacao_senha").css('visibility','hidden');
    }
    else{
        $("#confirmacao_senha").val("")
        $("#texto_confirmacao_senha").css('visibility','visible');
        $("#confirmacao_senha").css("border", "1px solid red")
    }
}

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

function fMasc(objeto,mascara) {
    obj=objeto
    masc=mascara
    setTimeout("fMascEx()",1)
    }

function fMascEx() {
obj.value=masc(obj.value)
}


function mCPF(cpf){
    cpf=cpf.replace(/\D/g,"")
    cpf=cpf.replace(/(\d{3})(\d)/,"$1.$2")
    cpf=cpf.replace(/(\d{3})(\d)/,"$1.$2")
    cpf=cpf.replace(/(\d{3})(\d{1,2})$/,"$1-$2")
    return cpf    
}

function mTel(tel){
    tel=tel.replace(/\D/g,"")
    tel=tel.replace(/(\d{1})/,"($1")
    tel=tel.replace(/(\d{1})(\d)/,"$1$2) ")
    tel=tel.replace(/(\d{5})(\d)/,"$1-$2")
    return tel
}

//04.946.087/0001-45
function mCNPJ(cnpj){
    cnpj=cnpj.replace(/\D/g,"")
    cnpj=cnpj.replace(/(\d{2})(\d)/,"$1.$2")
    cnpj=cnpj.replace(/(\d{3})(\d)/,"$1.$2")
    cnpj=cnpj.replace(/(\d{3})(\d{6})$/,"$1/$2")
    cnpj=cnpj.replace(/(\d{4})(\d{2})$/,"$1-$2")
    return cnpj
}

function idade(nascimento) {
    console.log(nascimento)
    var hoje = new Date
    var nascimento2 = new Date(nascimento)
    var diferencaAnos = hoje.getFullYear() - nascimento2.getFullYear();
    if ( new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate()) < 
        new Date(hoje.getFullYear(), nascimento2.getMonth(), nascimento2.getDate()) )
        diferencaAnos--;
    return diferencaAnos;
}

function checarIdade(nascimento){
    var anos = idade(nascimento)
    console.log(anos)
    if (anos<18){
        $("#data_nasc").css("border", "1px solid red")
        //alert("O cliente deve ser maior de idade!")
        $('#cadastro_cliente_maior_idade').css('display','inline')
        $("#data_nasc").val("")
        
    }
    else{
        $("data_nasc").css("border", "1px solid #ced4da")
    }
}

// //////////// MEDICAMENTOS   ////////////////////

