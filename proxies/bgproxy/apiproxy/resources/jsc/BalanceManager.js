var active = context.getVariable("private.active");
var inactive = active == "blue" ? "green" : "blue";

var canaryMode = context.getVariable("private.canary_mode") == "true";
var canaryBalance = Number(context.getVariable("private.canary_balance"));


// Set to 0 if for whatever reason there was a parse failure
if (isNaN(canaryBalance)) {
    canaryBalance = 0;
}

// Clamp canaryBalance so that it is between 0 and 100 inclusive
if (canaryBalance < 0) {
    canaryBalance = 0;   
}

if (canaryBalance > 100) {
    canarybalance = 100;
}

// Set which to route to go with
if (canaryMode && canaryBalance > 0) {
    // If canary mode is active, then we want to send canaryBalance% of requests to inactive.
    
    // We skip for 0 because Math.random could actually return 0, and we don't want to send
    // a request in that case.
    
    // If rolling lower than balance, send to inactive, otherwise active
    var chance = Math.random() * 100;
    if (chance <= canaryBalance) {
        context.setVariable("private.route_to", inactive)
    } else {
        context.setVariable("private.route_to", active);
    }
} else {
    context.setVariable("private.route_to", active);
}