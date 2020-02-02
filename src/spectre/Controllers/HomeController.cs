using Microsoft.AspNetCore.Mvc;

namespace spectre.Controllers
{
    [Route("/")]
    [ApiController]
    public class HomeController : ControllerBase
    {
        // GET: /
        [HttpGet]
        public RedirectResult Get()
        {
            return Redirect("index.html");
        }
    }
}
