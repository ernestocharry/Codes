c========================================================================
*
      program proj2b
*
c========================================================================
c     This code computes the bound and pseudostates of a two-body problem
c     (spinless core; uncharged fragment)
c     using a Lagrange-Legendre and a Lagrange-Laguerre basis.
c     14/05/14
c     Pesudostates wave functions --> fort.12
c     max. number of pseudostaes --> fort.13
c========================================================================
      implicit real*8 (a,b,d-h,o-z)
      implicit complex*16(c)
      allocatable wg(:),z(:),ham(:,:),ie(:),vec(:)
      allocatable EigenE(:), EigenVec(:,:), EigenVec1(:)
      allocatable d1(:), e1(:) 
      real xa, xb
c     
c     wg(n) : weight of each zero
c     z(n)  : zeros of the Lagrange functions
c     ham   : hamiltonian
c
      read*,n,a
c     Number of Lagrange func. and channel radius/scaling par

      if (a.lt.1) then
         h=a
         print*,'Lagrange Laguerre',' h (fm)=',h
      else
         print*,'Lagrange legendre','a (fm)=',a
      endif
      print*,'No. of Lagrange functions= ',n

      read*,ac,af
      read*,ns2
      read*,lmax,emax
!      write(12,*) n,a
!      write(12,*) ac,af
!      write(12,*) ns2 !2*sp (spinless core -> spin fragment)
!      write(12,2000) lmax,emax

      xmucf = 20.736*(ac+af)/(ac*af)
      print*,'xmucf=',xmucf

      allocate (wg(n),z(n),ham(n,n),ie(lmax),vec(n))
      allocate (EigenE(n), EigenVec(n,n),EigenVec1(n))
      allocate (d1(n), e1(n))

      if(a.lt.1) then
        itype = 1 !Lagrange-Laguerre
      else
        itype = 0 !Lagrange-Legendre
      endif

      xa     = 0
      xb     = 1
c-----------------------------------------------------------------------
c     Computing the Hamiltonian matrix elements
c-----------------------------------------------------------------------
      call LegendreAndLaguerre(itype,xa,xb,n,wg,z)



!      open(15,file='BePotential_l0_j1.txt')
!      open(16,file='BePotential_l1_j1.txt')
!      open(17,file='BePotential_l1_j3.txt')
      open(18,file='BeEnergies.txt')
      open(19,file='BeZerosWeight.txt')
      open(20,file='BeVectors.txt')
      open(21,file='BeNumberL.txt')

      do i = 1, n
        write(19,*) i, z(i),wg(i)
      end do

 1000 format(i5,f20.12,200es26.14)
 2000 format(i4,1x,f6.2)
 3000 format(i4,i4,i4)
      RHO = 1.0d-14

      print*, 'lamx', lmax

                  !Lagrange-Laguerre   
      do 88 l=0,lmax
        do 77 j2 = abs(2*l-ns2),2*l+ns2,2
            do 66 i=1,n
                do 55 j=1,n
                    if (i.eq.j) then
                        tl =((4+(4*n+2)*z(i)-z(i)**2)/(12*z(i)**2)
     &                        +l*(l+1)/z(i)**2)*xmucf/h**2
                        v =   potncf(j2,l,z(i)*h)
                        ham(i,j) = tl+v
                    else
                        fac    = (-1.)**(i-j)
                        aux1   = (z(i)+z(j))
                        aux2   =(z(i)*z(j))**(1/2.)*(z(i)-z(j))**2
                        tl     = xmucf*fac*aux1/(aux2*h**2)
                        v      = 0
                        ham(i,j) = tl+v
                    endif
 55             continue
 66         continue

            call tred2(ham,n,n,d1,e1)
            call tqli(d1,e1,n,n,ham)

            do i=1,n        ! Organizing the EigenE E1<E2<E2
                do j=i+1,n
                    if (d1(i).gt.d1(j)) then
                        t     = d1(j)
                        d1(j) = d1(i)
                        d1(i) = t
                        vec   = ham(:,j)
                        ham(:,j) = ham(:,i)
                        ham(:,i) = vec
                    endif
                enddo
            enddo

            NumberL = 0
            do i = 1, n
                if(d1(i).le.emax)then
                    write(18,*) l, j2, i, d1(i)
                    write(20,*) l, j2, i, d1(i)
                    NumberL = NumberL + 1
                    do j = 1, n
                        write(20,*) ham(j,i)
                        if(l.eq.0 .and. j2.eq.1 .and. i.eq.2)then
                            EigenVec1(j) = ham(j,i)
                            print*, d1(i), EigenVec1(j)
                        endif
                    enddo
                endif
            enddo
        write(21,*) l, j2, NumberL
 77     continue

 88   continue



      Rmin      = RHO  ! fm
      Rmax      = 25     ! fm
      NR         = 200
      DeltaN    = (Rmax-Rmin)/NR
      do 97 j = 1, NR+1
        r = DeltaN*(j-1) + Rmin
        PN = 1
        S1 = 0
        do 98 k = 1, n
            S1 = ((-1)**k)*(sqrt(z(k))/(r-z(k)))*EigenVec1(k) + S1
            PN = (r-z(k))*PN/z(k)
c            print*, 'S1,Pn,z(k)', S1, PN, z(k)
98      continue
        Psi = S1*PN*exp(-r/2)
        write(22,*) r, Psi
c        write(*,*) r, Psi, S1, PN
97    continue



      end program
c========================================================================
*
      function potncf(j2,l,s)
*
c========================================================================
c     Nuclear core-fragment potential
c     10Be+n potential (PRC70-064605-04)
c     l --> Orbital angular momentum between the fragment and the core
c     s --> 1/2 spin of the neutron
c     j2 =2j ;   |j-1/2|<=j<=l+1/2
c------------------------------------------------------------------------
      implicit real*8 (a,b,d-h,o-z)
      implicit complex*16(c) 

      ve   = 62.52
      vo   = 39.74
      vls  = 21
      a    = 0.6
      R0   = 2.585
  
      vn  = 1./(1.+exp((s-R0)/a))
      vls = -vls*vn**2*exp((s-R0)/a)/(a*s)
      if (mod(l,2).eq.0) then
         potcn = -vn*ve
      else
         potcn = -vn*vo
      endif
      if (j2.eq.(2*l+1)) then
         potncf = potcn+l*vls/2
      elseif (j2.eq.(2*l-1)) then
         potncf = potcn-(l+1)*vls/2
      endif
      
      return
      end function
c=========================================================================
c=========================================================================
      SUBROUTINE LegendreAndLaguerre(itype,x1,x2,n,w,x)

c     n : Number of Lagrange Functions
c     w : Weights
c     x : Zero or abscissas 

      
      INTEGER n, MAXIT
      REAL x1,x2l, al, ai, alpha
      REAL*8 w(n), x(n)
      DOUBLE PRECISION EPS
      PARAMETER (EPS=3.d-14, MAXIT = 150)
      INTEGER i,j,m, ist 
      DOUBLE PRECISION p1,p2,p3,pp,xl,xm,z,z1

c     MAXIT perphas it too much to much to Laguerre
      
      if(itype.eq.0)then        !Legendre
         
         m=(n+1)/2
         xm=0.5d0*(x2+x1)
         xl=0.5d0*(x2-x1)

         DO i=1,m
            z=cos(3.141592654d0*(i-.25d0)/(n+.5d0))

 1          p1=1.d0
            p2=0.d0

            DO kk=1,n
               p3=p2
               p2=p1
               p1=((2.d0*kk-1.d0)*z*p2-(kk-1.d0)*p3)/kk
            END DO

            pp=n*(z*p1-p2)/(z*z-1.d0)
            z1=z
            z=z1-p1/pp

            IF(abs(z-z1).gt.EPS)THEN
               goto 1
            END IF
            
            x(i)=xm-xl*z
            x(n+1-i)=xm+xl*z
            w(i)=2.d0*xl/((1.d0-z*z)*pp*pp)
            w(n+1-i)=w(i)
         END DO
      else if(itype.eq.1)then   !Laguerre
         alpha = 0
         do i=1,n
            if(i.eq.1)then
               z=(1.+alf)*(3.+.92*alf)/(1.+2.4*n+1.8*alf)
            else if(i.eq.2)then
               z=z+(15.+6.25*alf)/(1.+.9*alf+2.5*n)
            else
               ai=i-2
               z1 =(1.+2.55*ai)/(1.9*ai)
               z2 =(1.26*ai*alf)/(1.+3.5*ai)
               z3 =(z-x(i-2))/(1.+.3*alf)
               z=z+(z1+z2)*z3
            end if
            
            do its=1,MAXIT
               p1=1.d0
               p2=0.d0
               
               do j=1,n
                  p3=p2
                  p2=p1
                  p1=((2*j-1+alf-z)*p2-(j-1+alf)*p3)/j
               end do
               
               pp=(n*p1-(n+alf)*p2)/z
               z1=z
               z=z1-p1/pp
               
               if(abs(z-z1).le.EPS)goto 2
            end do
            
            print*,  'too many iterations in gaulag', i
            
 2          x(i)=z
            w(i)=exp(z)/(z*pp*pp)
         enddo
         return
      end if
      return
      END SUBROUTINE

c=========================================================================

c=====================================
      SUBROUTINE tred2(a,n,np,d,e)
      INTEGER n,np
      REAL*8 a(np,np),d(np),e(np)
      INTEGER i,j,k,l
      REAL f,g,h,hh,scale
      
      do 181 i=n,2,-1
         l=i-1
         h=0.
         scale=0.
         if(l.gt.1)then
            do 111 k=1,l
               scale=scale+abs(a(i,k))
 111        continue
            if(scale.eq.0.)then
               e(i)=a(i,l)
            else
               do 121 k=1,l
                  a(i,k)=a(i,k)/scale
                  h=h+a(i,k)**2
 121           continue
               f=a(i,l)
               g=-sign(sqrt(h),f)
               e(i)=scale*g
               h=h-f*g
               a(i,l)=f-g
               f=0.
               do 151 j=1,l
                  a(j,i)=a(i,j)/h
                  g=0.
                  do 131 k=1,j
                     g=g+a(j,k)*a(i,k)
 131              continue 
                  do 141 k=j+1,l
                     g=g+a(k,j)*a(i,k)
 141              continue 
                  e(j)=g/h
                  f=f+e(j)*a(i,j)
 151           continue
               hh=f/(h+h)
               do 171 j=1,l
                  f=a(i,j)
                  g=e(j)-hh*f
                  e(j)=g
                  do 161 k=1,j
                     a(j,k)=a(j,k)-f*e(k)-g*a(i,k)
 161              continue
 171           continue 
            endif
         else
            e(i)=a(i,l)
         endif
         d(i)=h
 181  continue
      d(1)=0.
      e(1)=0.
      do 241 i=1,n
         l=i-1
         if(d(i).ne.0.)then
            do 221 j=1,l
               g=0.
               do 191 k=1,l
                  g=g+a(i,k)*a(k,j)
 191           continue
               do 211 k=1,l
                  a(k,j)=a(k,j)-g*a(k,i)
 211           continue
 221        continue
         endif
         d(i)=a(i,i)
         a(i,i)=1.
         do 231 j=1,l
            a(i,j)=0.
            a(j,i)=0.
 231     continue
 241  continue
      return
      END
c==============================================
      SUBROUTINE tqli(d,e,n,np,z)
      INTEGER n,np
      REAL*8 d(np),e(np),z(np,np)
      INTEGER i,iter,k,l,m
      REAL*8 b,c,dd,f,g,p,r,s
   
      do 11 i=2,n
         e(i-1)=e(i)
 11   continue
      e(n)=0.
      do 15 l=1,n
         iter=0
 1       do 12 m=l,n-1
            dd=abs(d(m))+abs(d(m+1))
            if (abs(e(m))+dd.eq.dd) goto 2
 12      continue
         m=n
 2       if(m.ne.l)then
!            if(iter.eq.30) pause 'too many iterations in tqli'
            iter=iter+1
            g=(d(l+1)-d(l))/(2.*e(l))
            r=sqrt(g**2+1.)
            g=d(m)-d(l)+e(l)/(g+sign(r,g))
            s=1.
            c=1.
            p=0.
            do 14 i=m-1,l,-1
               f=s*e(i)
               b=c*e(i)
               r=sqrt(f**2+g**2)
               e(i+1)=r
               if(r.eq.0.)then
                  d(i+1)=d(i+1)-p
                  e(m)=0.
                  goto 1
               endif
               s=f/r
               c=g/r
               g=d(i+1)-p
               r=(d(i)-g)*s+2.*c*b
               p=s*r
               d(i+1)=g+p
               g=c*r-b
               do 13 k=1,n
                  f=z(k,i+1)
                  z(k,i+1)=s*z(k,i)+c*f
                  z(k,i)=c*z(k,i)-s*f
 13            continue
 14         continue
            d(l)=d(l)-p
            e(l)=g
            e(m)=0.
            goto 1
         endif 
 15   continue
      return  
      END
