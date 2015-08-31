import pyproj
import math

class CoordUtils:
    @staticmethod
    def stateplane_for_latlng(latlng,epsg="2908"):
        """
        Function accepts a latlng co-ordinate and returns a stateplane co-ordinate
        -- latlng is a set in the form of (latitude,longitude)
        -- stateplane is a set in the form of (easting,northing)
        -- EPSG is the stateplane identifier which defaults to the identifier for Manhattan:
                EPSG:2908: NAD83(HARN) / New York Long Island (ftUS)
        """
        lat,lng = latlng[0], latlng[1]
        sp_epsg = "EPSG:"+epsg
        # Preserve units keeps projection in ftUS
        stateplane_projection = pyproj.Proj(init=sp_epsg, preserve_units=True)
        wgs84_projection = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        stateplane = pyproj.transform(wgs84_projection,stateplane_projection,lng,lat)
        return stateplane

    @staticmethod
    def latlng_for_stateplane(stateplane,epsg="2908"):
        """
        Function accepts a stateplane co-ordinate and returns a latlng coordinate set
        -- latlng is a set in the form of (latitude,longitude)
        -- stateplane is a set in the form of (easting,northing)
        -- EPSG is the stateplane identifier which defaults to the identifier for Manhattan:
                EPSG:2908: NAD83(HARN) / New York Long Island (ftUS)
        """
        easting, northing = stateplane[0], stateplane[1]
        sp_epsg = "EPSG:"+epsg 
        # Preserve units keeps projection in ftUS
        stateplane_projection = pyproj.Proj(init=sp_epsg, preserve_units=True)
        wgs84_projection = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        longlat = pyproj.transform(stateplane_projection,wgs84_projection,easting,northing)
        # flip longLat to latlng
        return (longlat[1],longlat[0])
        
        
    @staticmethod
    def waypoints_for_linestring(linestring,waypoint_distance_in_feet=32):
        
        """ 
        PARAMS:
        1. linestring - set containing two latlng coordinate pairs
        2. waypoint_distance_in_feet - distance between waypoints in feet. Default is set to 32.
        
        RETURN VALUE: 
        List of latlng sets for waypoints on the linestring
        
        Example line string objects from the streets database:
        ((40.6853, -73.9807), (40.686, -73.9803))
        ((40.7265, -73.874), (40.7264, -73.8739))
        ((40.7645, -73.7911), (40.7635, -73.7913))
        """
        
        latlng_1 = linestring[0]
        latlng_2 = linestring[1]
        
        # Convert from latlng to stateplane
        stateplane_1 = CoordUtils.stateplane_for_latlng(latlng_1)
        stateplane_2 = CoordUtils.stateplane_for_latlng(latlng_2)
        
        """Subtracting the northings gives you the distance in feet (since our SP projection 
        is in feet) from north to south.
        Subtracting the eastings gives you the distance in feet from east to west.
        For small distances, the distance over earth is equal to the euclidean distance 
        between the easting-northing coordinates
        """
        
        E1, N1 = stateplane_1[0], stateplane_1[1]
        E2, N2 = stateplane_2[0], stateplane_2[1]
        
        # Pythagorean theorum to find total distance
        total_distance = math.sqrt((N1-N2)**2+(E1-E2)**2)
        
        """        
        # Find the slope
        """
        y_total = N1 - N2 
        x_total = E1 - E2         
        
        slope = y_total/x_total;
        
        """
        # Step will keep track of how many steps we take between point 1 to 2
        # List will store the latlng set for each waypoint
        """
        step = 0
        waypoint_list = []
        
        """ 
        # Start walking from from point 1 to point 2
        # Each step moves us waypoint_distance_in_feet closer to point 2
        # We keep going until we meet/exceed total_distance
        """
        while (waypoint_distance_in_feet*step) < total_distance:
            h = waypoint_distance_in_feet*step
            dx = abs(math.sqrt(h**2/((slope**2)+1)))
            dy = abs(slope*dx)
            new_n = (N1-dy) if N1>N2 else (N1+dy)
            new_e = (E1-dx) if E1>E2 else (E1+dx)
            waypoint_list.append(CoordUtils.latlng_for_stateplane((new_e,new_n)))
            step = step + 1

        return waypoint_list
