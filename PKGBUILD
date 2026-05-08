# Maintainer: Baked Beans <contact@bkd.lol>
pkgname=bmsg
pkgver=0.4.3
pkgrel=1
pkgdesc="Simple Message Encryption Application"
arch=(any)
url="https://bmsg.bkd.lol"
license=('custom:ISL-v0.3')
depends=('python>=3.9.0')
options=()
install=
changelog=
source=("$pkgname-$pkgver.tar.gz"
        "$pkgname-$pkgver.patch")
noextract=()
sha256sums=()
validpgpkeys=()

prepare() {
	cd "$pkgname-$pkgver"
	patch -p1 -i "$srcdir/$pkgname-$pkgver.patch"
}

build() {
	cd "$pkgname-$pkgver"
	./configure --prefix=/usr
	make
}

check() {
	cd "$pkgname-$pkgver"
	make -k check
}

package() {
	cd "$pkgname-$pkgver"
	make DESTDIR="$pkgdir/" install
}
