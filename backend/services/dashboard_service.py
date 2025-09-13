from models.data import shipments, vehicles, clients

def get_dashboard_stats():
    total_shipments = len(shipments)
    pending = len([s for s in shipments if s.status == "Pending"])
    in_transit = len([s for s in shipments if s.status == "In Transit"])
    delivered = len([s for s in shipments if s.status == "Delivered"])
    total_vehicles = len(vehicles)
    available_vehicles = len([v for v in vehicles if v.status == "Available"])
    total_clients = len(clients)
    
    return {
        "shipments": {
            "total": total_shipments,
            "pending": pending,
            "in_transit": in_transit,
            "delivered": delivered
        },
        "vehicles": {
            "total": total_vehicles,
            "available": available_vehicles
        },
        "clients": {
            "total": total_clients
        }
    }