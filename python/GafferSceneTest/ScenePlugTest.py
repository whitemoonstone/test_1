##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

import unittest

import IECore

import Gaffer
import GafferScene
import GafferSceneTest

class ScenePlugTest( unittest.TestCase ) :

	def testRunTimeTyped( self ) :
	
		p = GafferScene.ScenePlug()
		
		self.failUnless( p.isInstanceOf( Gaffer.CompoundPlug.staticTypeId() ) )	
		self.assertEqual( IECore.RunTimeTyped.baseTypeId( p.typeId() ), Gaffer.CompoundPlug.staticTypeId() )
	
	def testDynamicSerialisation( self ) :
	
		s = Gaffer.ScriptNode()
		s["n"] = Gaffer.Node()
		s["n"]["p"] = GafferScene.ScenePlug( flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic )
		
		ss = s.serialise()
				
		s = Gaffer.ScriptNode()
		s.execute( ss )
	
	def testFullTransform( self ) :
	
		translation = IECore.M44f.createTranslated( IECore.V3f( 1 ) )
		scaling = IECore.M44f.createScaled( IECore.V3f( 10 ) )
	
		n = GafferSceneTest.CompoundObjectSource()
		n["in"].setValue(
			IECore.CompoundObject( {
				"children" : {
					"group" : {
						"transform" : IECore.M44fData( translation ),
						"children" : {
							"ball" : {
								"transform" : IECore.M44fData( scaling ),			
							}
						}
					},
				},
			} )
		)
		
		self.assertEqual( n["out"].transform( "/" ), IECore.M44f() ) 
		self.assertEqual( n["out"].transform( "/group" ), translation )
		self.assertEqual( n["out"].transform( "/group/ball" ), scaling )
		
		self.assertEqual( n["out"].fullTransform( "/" ), IECore.M44f() )
		self.assertEqual( n["out"].fullTransform( "/group" ), translation )
		
		m = n["out"].fullTransform( "/group/ball" )
		self.assertEqual( m.translation(), IECore.V3f( 1 ) )
		self.assertEqual( m.extractScaling(), IECore.V3f( 10 ) )
		self.assertEqual( m, scaling * translation )
		
if __name__ == "__main__":
	unittest.main()
	
