import config, random, math
import pybrain


class Main:
	def __init__( self ):
		pass


class Environment:
	def __init__( self ):
		
		# init placeholder
		self.members = []
		self.targets = []

		# init members and targets
		self.members = [ self.add_new_member() for i in range(config.population_size) ]
		self.targets = [ self.add_new_target() for i in range(config.target_count) ]

	def add_new_member( self ):
		new_member 		= Member()
		x,y 			= Helper.nonintersecting_coordinates( new_member.radius, self.get_positions() )
		new_member.x  	= x
		new_member.y 	= y
		return new_member

	def add_new_target( self ):
		new_target 		= Target()
		x,y 			= Helper.nonintersecting_coordinates( new_target.radius, self.get_positions() )
		new_target.x  	= x
		new_target.y 	= y
		return new_target

	def get_objects( self ):
		return self.members + self.targets

	def get_positions( self ):
		return [[obj.x,obj.y] for obj in self.get_objects()]


class Member:

	max_energy = config.member_max_energy

	def __init__( self ):
		self.radius 	 = config.member_radius
		self.color  	 = Helper.random_color()

		self.brain       = Brain()

		self.x 			 = None
		self.y 			 = None

		self.energy      = self.max_energy
		self.distance    = 0.0
		self.relation    = 0.0
		self.rotation    = 0.0
		self.speed       = 0.0

		self.left_track  = None
		self.right_track = None

		self.close_to    = None

	def update_member_state( self ):
		self.process_network()
		self.rotation += (self.left_track - self.right_track) / self.radius
		if self.rotation > (2 * math.pi): self.rotation = 0
		elif self.rotation < 0: self.rotation = (2 * math.pi)
		self.speed = self.left_track + self.right_track

	def update_member_position( self ):

		x_move = self.x + Helper.delta_x( self.rotation, self.speed )
		y_move = self.y + Helper.delta_y( self.rotation, self.speed )

		if x_move > config.viewport_width: x_move = 0
		elif x_move < 0: x_move = config.viewport_width

		if y_move > config.viewport_height: y_move = 0
		elif y_move < 0: y_move = config.viewport_height

		self.x = move_x
		self.y = move_y
	
	def process_network( self ):
		self.left_track, self.right_track = self.brain.activate_network(self.get_params())

	def get_params( self ):
		energy_input = ( 1 - ( 1 / self.energy ))
		return [ energy_input, distance, relation ]


class Target:
	def __init__( self ):
		self.radius = config.target_radius
		self.color  = config.target_color
		self.x = None
		self.y = None


class Brain:
	def __init__( self ):
		self.network = self.build_network()

	def build_network( self ):
		net 		 = FeedForwardNetwork()
		input_layer  = LinearLayer( 3 )
		logic_layer  = LinearLayer( 1 )
		output_layer = TanhLayer( 2 )
		net.addInputModule( input_layer )
		net.addModule( logic_layer )
		net.addOutputModule( output_layer )
		net.addConnection(FullConnection( input_layer, logic_layer ))
		net.addConnection(FullConnection( logic_layer, output_layer ))
		net.sortModules()
		return net

	def activate_network( self, params ):
		if params:
			return self.network.activate( params )


class Database:
	def __init__( self ):
		pass


class Helper:
	
	@staticmethod
	def fixed(a): 		return int(round(a))

	@staticmethod
	def delta_x(a,b): 	return math.sin(a) * b

	@staticmethod
	def delta_y(a,b): 	return math.cos(a) * b

	@staticmethod
	def random_color(): return [ random.randint(config.color_min, config.color_max) for i in range(3) ]

	@staticmethod
	def collided(a,b): 	return Helper.slope([a.x,a.y],[b.x,b.y]) < (a.radius + b.radius)

	@staticmethod
	def track_differential(a,b,c): return ((a - b) / c)

	@staticmethod
	def track_speed(a,b): return a + b

	@staticmethod
	def slope(a,b):
		dx = a[0] - b[0]
		dy = a[1] - b[1]
		return math.fabs(math.hypot(dx,dy))

	@staticmethod
	def relation(a,b):
		dx = a[0] - b[0]
		dy = a[1] - b[1]
		return math.atan2(dx,dy)

	@staticmethod
	def nonintersecting_coordinates(radius,positions):
		x,y = [
			random.randint(radius,config.viewport_width-radius), 
			random.randint(radius,config.viewport_height-radius)
		]
		for pos in positions:
			if Helper.slope([x,y],[pos[0],pos[1]]) < (radius + config.intersection_tolerance):
				Helper.nonintersecting_coordinates(radius, objects)
		return [x,y]


