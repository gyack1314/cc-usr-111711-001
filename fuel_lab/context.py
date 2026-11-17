"""解释已取得原文中的机场加注覆盖业务上下文。"""
from .evidence import records

def snapshot(db,known_at):
    rows=records(db,'context',known_at)
    if not rows:return None
    p=rows[-1]['payload']
    return {'airport':p['airport'],'receipt_units':p['receipt_units'],'claimable_units':p['claimable_units'],'flight_departure':p['flight_departure']}

def eligible(s,d,state,period):
    if state is None:return False,'缺少业务上下文'
    return (s.get('airport',state['airport'])==d.get('departure_airport',state['flight_departure']), '加注机场与出发机场不一致')

def metrics(allocations,state,period):
    if state is None:return {'context_gap':'缺少业务上下文'}
    return {'physical_receipt_gap':max(0,state['receipt_units']-sum(x['quantity'] for x in allocations)),'claimable_units':state['claimable_units']}
