//检查数据规格
const regs = {
    email: /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/,
    number: /^([0]|[1-9][0-9]*)$/,
    password: /^(?=.*\d)(?=.*[a-zA-Z])[\da-zA-Z~!@#$%^&*_]{8,}$/,
    shareCode: /^[A-Za-z0-9]+$/
}
const vertify = (rule, value, reg, callback) => {
    if(value) {
        if (reg.test(value)) {
            callback()
        } else {
            callback(new Error(rule.message))
        }
    } else {
        callback()
    }
}

export default {
    number: (rule, value, callback) => {
        return vertify(rule, value, regs.number, callback)
    },
    password: (rule, value, callback) => {
        return vertify(rule, value, regs.password, callback)
    },
    
}