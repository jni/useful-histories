---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Payback period of two electric heat pumps

Hydronic heating works by providing heat energy to the home in the form of hot water, which is radiated inside the house. We can heat the water either by using a gas boiler, or an air-to-water heat pump. The gas boilers have a coefficient of performance (COP) of approximately 0.7, which means that 70% of the gas energy put in makes it as heat into the water (and thus the house). The Stiebel Eltron AC25 heat pump has a COP of 5, which means that for every watt of electricity put in, you get 5 watts of heat out (!). This is achieved by harvesting ambient heat from the air (and produces colder air outside as a by-product).

The issue is that heat pumps are more expensive than gas boilers. In this case, we will assume a 3K AUD gas boiler faced against a 15K AUD heat pump.

We'll use the [pint](https://pint.readthedocs.io/en/stable/) library to convert units and figure out how many years of heating we need to make back the cost of the heat pump.

```{code-cell} ipython3
import pint

u = pint.UnitRegistry()
u.define('dollar = [currency]')
u.define('cent = 0.01 * dollar')
gas_price = 1.78 * u('cent / MJ')  # based on current prices 2022-05-23
elec_price = 20.35 * u('cent / kWh')  # based on current prices
```

Now we have the basic gas prices and electricity prices. To figure out how much it costs to get a kWh of heat using gas vs electricity, we divide the above values by the COP of each technology.

```{code-cell} ipython3
gas_heat_price = gas_price / 0.7
elec_heat_price = elec_price / 5

print('gas cost of heat: ', gas_heat_price.to('cent / kWh'))
print('electric heat pump cost of heat: ', elec_heat_price.to('cent / kWh'))
```

Now, how much heat does one need in a year? I am basing this my gas usage from last year from April to November, inclusive. In that time, I used 80,000 MJ of gas in addition to the summer baseline (ie cooktop, hot water). Given the cop, that means I needed 80,000 $\times$ 0.7 MJ of heat:

```{code-cell} ipython3
annual_usage = 80_000 * 0.7 * u('MJ / year')
```

Finally, we multiply this by the cost per megajoule to get the annual cost.

```{code-cell} ipython3
annual_cost_gas = annual_usage * gas_heat_price
annual_cost_elec = annual_usage * elec_heat_price

print('the annual cost of gas heating is: ', annual_cost_gas.to('dollar / year'))
print('the annual cost of electric heating is: ', annual_cost_elec.to('dollar / year'))

annual_savings = (annual_cost_gas - annual_cost_elec).to('dollar / year')

print('annual savings: ', annual_savings)
```

The payback period is therefore:

```{code-cell} ipython3
print('the payback period is: ', 12_000 * u.dollar / annual_savings)
```

It's important to note that this calculation is done without accounting for heating powered by rooftop solar panels — in this case, we get additional savings equal to about 8c/kWh (difference between feed-in tariff and cost of electricity). Therefore, the above payback period represents an upper bound.
