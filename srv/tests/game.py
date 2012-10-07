#!/usr/bin/python

import unittest

from srv.registry import registry
from logic.dice import Dice
from srv.inout.inout import InOut

from xml.dom.minidom import parseString

registryxml="""<registry>
	<enum name="games">
		<value id="0" name="inout"/>
		<value id="1" name="dice"/>
	</enum>
	<enum name="phases">
		<value id="0" name="inout"/>
		<value id="11" name="dicedoubler"/>
		<value id="12" name="dicewithdraw"/>
		<value id="13" name="dice"/>
	</enum>
	<enum name="variables">
		<value id="0" name="credit"/>
		<value id="1" name="outmoney"/>
		<value id="2" name="inmoney"/>
		<value id="101" name="betcolor"/>
		<value id="102" name="outcolor"/>
		<value id="103" name="doubledamount"/>
		<value id="131" name="diceingame"/>
		<value id="132" name="holddice1"/>
		<value id="133" name="holddice2"/>
		<value id="134" name="holddice3"/>
		<value id="135" name="bet"/>
		<value id="136" name="dice1state"/>
		<value id="137" name="dice2state"/>
		<value id="138" name="dice3state"/>
	</enum>
	<game name="inout">
		<phase name="inout">
			<variable account="true" id="credit" output="true"/>
			<variable id="outmoney" input="true"/>
			<variable id="inmoney" input="true"/>
		</phase>
	</game>
	<game name="dice">
		<phase name="dicewithdraw">
			<variable account="true" id="credit" output="true"/>
			<variable account="true" id="diceingame"/>
		</phase>
		<phase name="dice">
			<variable account="true" id="credit"/>
			<variable account="true" id="diceingame" output="true"/>
			<variable id="holddice1" input="true"/>
			<variable id="holddice2" input="true"/>
			<variable id="holddice3" input="true"/>
			<variable id="bet" input="true"/>
			<variable id="dice1state" output="true"/>
			<variable id="dice2state" output="true"/>
			<variable id="dice3state" output="true"/>
		</phase>
		<phase name="dicedoubler">
			<variable account="true" id="diceingame"/>
			<variable id="betcolor" input="true"/>
			<variable id="outcolor" output="true"/>
			<variable id="doubledamount" output="true"/>
		</phase>
	</game>
</registry>
"""

class TestGame(unittest.TestCase):

	def test_game(self):
		d = Dice()
		i = InOut()
		r = registry.toDom().toprettyxml()
		#print r
		self.assertEqual(r,registryxml)
		self.assertEquals(registry.getGameById(0), i)
		dice = registry.getGameByName("dice")
		self.assertEqual(dice, registry.getGameById(1))

	def test_play(self):
		dicephase = registry.getPhaseByName("dice")
		state = {131:10, 135:10, 132:0, 133:0,134:0}
		class record:
			pass
		state=record()
		state.credit = 10
		state.diceingame = 10
		state.holddice1 = 0
		state.holddice2 = 0
		state.holddice3 = 0
		state.dice1state = 0
		state.dice2state = 0
		state.dice3state = 0
		state.bet = 10
		dicephase.play(state)
		#print state.__dict__

if __name__ == '__main__':
	unittest.main()

