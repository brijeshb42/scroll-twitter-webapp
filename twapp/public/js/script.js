(function($){
	var LOADING = 'Loading link info...';
	$(document).ready(function(){
		$('span.datalink').on('click',function(){
			var $this = $(this);
			if($this.data('fetched')==0){
				$this.hide();
				var id = $this.data('id');
				var ltitle = $('#link-title-'+id);
				var ldesc = $('#link-desc-'+id);
				ltitle.html(LOADING);
				ldesc.html('');
				$.get('/scrape/?url='+$this.data('url'),function(data){
					if(data.type && data.type === 'success'){
						ltitle.html(data.title);
						ldesc.html(data.desc);
					}else{
						ltitle.html(data.title)
					}
				})
			}
		});

	});
})(jQuery);