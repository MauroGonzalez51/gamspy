Set factories(*);
Set clients(*);
Parameter offer(factories);
Parameter demand(clients);
Parameter cost(factories,clients);
positive Variable x(factories,clients);
Equation supply_equation(factories);
Equation demand_equation(clients);
free Variable transport_objective_variable;
Equation transport_objective;
Model transport / supply_equation,demand_equation,transport_objective /;
$gdxLoadAll /home/arch/dev/python/gamspy/gams/transport_data.gdx
supply_equation(factories) .. sum(clients,x(factories,clients)) =l= offer(factories);
demand_equation(clients) .. sum(factories,x(factories,clients)) =g= demand(clients);
transport_objective .. sum((factories,clients),(cost(factories,clients) * x(factories,clients))) =e= transport_objective_variable;
solve transport using LP MIN transport_objective_variable;